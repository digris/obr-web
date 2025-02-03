#! /usr/bin/env liquidsoap

settings.log.stdout.set(true)
settings.log.level.set(2)
settings.log.unix_timestamps.set(false)

settings.frame.audio.samplerate.set(44100)
settings.frame.audio.channels.set(2)
interactive.harbor(
    port=5006,
)

# keep reference of process start
time_start = time()

s_news_playing = ref(false)

j_opener = "recorded/opener.mp3"
j_closer = "recorded/closer.mp3"

# s = mksafe(input.http(
# #   "http://maxxima.mine.nu/maxxima.mp3",
#   "http://stream.srg-ssr.ch/m/SRF_news/aacp_96",
# ))

s = mksafe(playlist("mock/ref/"))


#######################################################################
# helpers & debug
#######################################################################

def time_up()
  round(time() - time_start)
end



#######################################################################
# jingle insertion queues
#######################################################################

s_queue = request.queue(
  id="s_queue",
)

sf_queue = request.queue(
  id="sf_queue",
)



#######################################################################
# detection handling
#######################################################################

def on_begin_detect()
  print("#{time_up()} - on_start_detect");
end


def on_end_detect()
  print("#{time_up()} - on_start_detect");
end



#######################################################################
# signal tetection
#######################################################################

s = sine.detect(
  debug=false,
  smoothing=0.01,
  duration=2.0,
  threshold=10.0,
  bands=1024,
  [
    1000.0,
  ],
  s,
  fun(k) -> begin

    print("#{time_up()} - sine: #{k}");

    # sine detected: we know emission will start in 4s from now
    thread.run(
      # delay=4.0,
      delay=3.5,
      fun() -> begin
        print("#{time_up()} - source:news: will start in 5s");
        s_news_playing.set(true);
      
        # enqueue opener
        sf_queue.push(
          request.create(
            j_opener
          )    
        );
      end
    )

    # as we have a buffer, actual audio starts 5s later ;)
    thread.run(
      delay=9.0,
      fun() -> begin
        print("#{time_up()} - source:news: playing");
      end
    )
  end
)


s = blank.detect(
  # max_blank=5.0,
  max_blank=4.0,
  min_noise=1.0,
  threshold=-40.0,
  track_sensitive=false,
  fun() -> begin
    # print("#{time_up()} - blank");
    if s_news_playing() == true then
      # print("#{time_up()} - source:news: end 5s before now");
      print("#{time_up()} - source:news: end");
      s_news_playing.set(false);

      # enqueue closer
      sf_queue.push(
        request.create(
          j_closer
        )    
      );
    else
      print("#{time_up()} - source:news: blank detected");
    end
  end,
  s
)



#######################################################################
# debug
#######################################################################

s = rms(s)
def print_rms()
  l = s.rms()
  r = dB_of_lin(l)
  print("RMS: #{round(r)} dB - LIN: #{l}")
end
# thread.run(every=1., print_rms)


#######################################################################
# jingle insertion & delayed "final" source
#######################################################################


s = smooth_add(
  normal=s,
  special=s_queue,
  p=.01,
)




sf = buffer(
  buffer=5.0,
  max=5.0,
  s,
)


sf = smooth_add(
  normal=sf,
  special=sf_queue,
  p=.01,
)


#######################################################################
# encoding
#######################################################################
aac_48 = %ffmpeg(
  format="mpegts",
  %audio(
    channels=2,
    samplerate=44100,
    codec="aac",
    b="48k",
    profile="aac_low"
  )
)

aac_196 = %ffmpeg(
  format="mpegts",
  %audio(
    channels=2,
    samplerate=44100,
    codec="aac",
    b="196k",
    profile="aac_low"
  )
)

# LS: v2.2
# def hls_segment_name(~position,~extname=_,stream_name) =
#   timestamp = int_of_float(time())
#   "#{stream_name}-#{timestamp}-#{position}.ts"
# end

# LS: v2.3
def hls_segment_name(metadata) =
  timestamp = int_of_float(time())
  "#{metadata.stream_name}-#{timestamp}-#{metadata.position}.ts"
end


#######################################################################
# output
#######################################################################

output.harbor.hls(id="output_hls",
  port=5005,
  playlist="manifest.m3u8",
  segment_duration=6.0,
  segments=5,
  segments_overhead=5,
  segment_name=hls_segment_name,
  [
    ("aac_196", aac_196),
    ("aac_48", aac_48),
  ],
  s
)

# output.file.hls(id="output_hls",
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
#   s
# )


output(sf)