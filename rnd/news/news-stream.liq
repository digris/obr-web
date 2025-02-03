#! /usr/bin/env liquidsoap

settings.log.stdout.set(true)
settings.log.level.set(2)
settings.log.unix_timestamps.set(false)

settings.frame.audio.samplerate.set(44100)
settings.frame.audio.channels.set(2)

# keep reference of process start
time_start = time()

news_source_active = ref(false)
news_final_source_amplify = ref(0.0)

jingle_opener = "recorded/opener-5s.mp3"
jingle_closer = "recorded/closer.mp3"

sse_url = "https://openbroadcast.ch/sse"

# news_source = mksafe(input.http(
#   "http://stream.srg-ssr.ch/m/SRF_news/aacp_96",
# ))

news_source = mksafe(playlist("mock/ref/"))
# news_final (see below)


#######################################################################
# helpers & debug
#######################################################################

def time_up()
  # round(time() - time_start)
  time() - time_start
end



#######################################################################
# jingle insertion queues
#######################################################################

news_source_queue = request.queue()
news_final_queue = request.queue()



#######################################################################
# detection handlers
# see: README.md - "Signaling"
#######################################################################

def sse_publish(cmd, payload = {})
  #<
  publish event to SSE publisher API
  >#

  print("#{time_up()} - SSE: #{cmd} - #{payload}");

  uri = "#{sse_url}/news"
  print("POST: #{uri}")
  h = http.post(
    headers=[
      ("user-agent", "test"),
      ("Content-Type", "application/json; charset=UTF-8"),
    ],
    data=json.stringify({
      cmd=cmd,
      ...payload
    }),
    uri
  )
  if h.status_code == 204 then
    print("SSE: #{cmd} - OK")
  end
  if h.status_code >= 400 then
    log.important("failed to publish sse event: #{h.status_code} - #{h}")
  end

end

def on_begin_detected(_)
  #<
  
  signal is detected:
  - 4s BEFORE the news start in SOURCE-STREAM
  - 4s BEFORE the opener jingle start in FINAL-STREAM
  - 9s BEFORE the news start in FINAL-STREAM

  set the following "delayed" tasks:
  - 2s un-mute final source feed
  - 4s start opener jungle (5s)
  - 4?s notify API

  >#

  print("#{time_up()} - detected:begin");

  thread.run(
    #################################################################
    delay=2.0,
    #################################################################
    fun() -> begin
      print("#{time_up()} - final-queue: set amplify to 1.0");
      news_final_source_amplify.set(1.0);
    end
  )

  thread.run(
    #################################################################
    delay=4.0,
    #################################################################
    fun() -> begin
      print("#{time_up()} - final-queue: start opener");
      news_final_queue.push(
        request.create(jingle_opener)    
      );
    end
  )

  thread.run(
    #################################################################
    delay=4.0,
    #################################################################
    fun() -> begin
      sse_publish(
        "start",
        {
          ts=time(),
          provider="srf"
        }
      );
    end
  )

  news_source_active.set(true);

end


def on_end_detected()
  #<
  
  signal is detected:
  - 4s AFTER the news ended in SOURCE-STREAM
  - 1s BEFORE the news will end in FINAL-STREAM
  - 6s BEFORE the closer jingle will end in FINAL-STREAM

  set the following "delayed" tasks:
  - 1s start closer jungle (5s)
  - 10s mute final source feed
  - 7?s notify API

  >#
  
  if news_source_active() == false then

    print("#{time_up()} - detected:blank - no source active");

  else

    print("#{time_up()} - detected:end");
    
    thread.run(
      #################################################################
      delay=1.0,
      #################################################################
      fun() -> begin
        print("#{time_up()} - final-queue: start closer");
        news_final_queue.push(
          request.create(jingle_closer)
        );
      end
    )

    thread.run(
      #################################################################
      delay=10.0,
      #################################################################
      fun() -> begin
        print("#{time_up()} - final-queue: set amplify to 0.0");
        news_final_source_amplify.set(0.0);
      end
    )

    thread.run(
      #################################################################
      delay=7.0,
      #################################################################
      fun() -> begin
        sse_publish(
          "stop",
          {
            ts=time(),
            provider="srf"
          }
        );
      end
    )
  
    news_source_active.set(false);

  end

end



#######################################################################
# in-band signaling detection
#######################################################################

news_source = sine.detect(
  duration=2.0,
  smoothing=0.01,
  threshold=10.0,
  bands=1024,
  [1000.0,],
  news_source,
  on_begin_detected
)


news_source = blank.detect(
  max_blank=4.0,
  min_noise=1.0,
  threshold=-40.0,
  start_blank=true,
  track_sensitive=false,
  on_end_detected,
  news_source
)



#######################################################################
# debug
#######################################################################
# 
# news_source = rms(news_source)
# def print_rms()
#   l = news_source.rms()
#   r = dB_of_lin(l)
#   print("RMS: #{round(r)} dB - LIN: #{l}")
# end
# thread.run(every=1., print_rms)


#######################################################################
# jingle insertion & delayed "final" source
#######################################################################


news_source = smooth_add(
  normal=news_source,
  special=news_source_queue,
  p=.01,
)



#######################################################################
# final source
#######################################################################

#<
final source is in a fixed 5s buffer
>#
news_final = buffer(
  buffer=5.0,
  max=5.0,
  amplify(
    news_final_source_amplify,
    news_source
  )
)


news_final = smooth_add(
  normal=news_final,
  special=news_final_queue,
  p=.01,
)


#######################################################################
# HLS / output
#######################################################################


# LS: v2.2
def hls_segment_name(~position,~extname=_,stream_name) =
  timestamp = int_of_float(time())
  "#{stream_name}-#{timestamp}-#{position}.ts"
end

# LS: v2.3
# def hls_segment_name(metadata) =
#   timestamp = int_of_float(time())
#   "#{metadata.stream_name}-#{timestamp}-#{metadata.position}.ts"
# end


#######################################################################
# output
#######################################################################

output.harbor.hls(
  port=5005,
  playlist="manifest.m3u8",
  segment_duration=1.0,
  segments=5,
  segments_overhead=5,
  segment_name=hls_segment_name,
  [
    (
      "aac_96",
      %ffmpeg(
        format="mpegts",
        %audio(
          channels=2,
          samplerate=44100,
          codec="aac",
          b="96k",
          profile="aac_low"
        )
      )
    ),
  ],
  news_final
)

# output.file.hls(
#   "/Users/ohrstrom/code/obr-web/playground/news/hls",
#   playlist="manifest.m3u8",
#   segment_duration=1.0,
#   segments=5,
#   segments_overhead=5,
#   segment_name=hls_segment_name,
#   [
#     ("aac_196", aac_196),
#     ("aac_48", aac_48),
#   ],
# #   [("mp3-low", %mp3(bitrate=96)), ("mp3-hi", %mp3(bitrate=160))],
#   news_final
# )


# output(news_source)
# output(news_final)