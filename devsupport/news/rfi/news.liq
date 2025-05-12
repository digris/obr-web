#! /usr/bin/env liquidsoap

settings.log.stdout.set(true)
settings.log.level.set(2)
settings.log.unix_timestamps.set(false)

settings.frame.audio.samplerate.set(44100)
settings.frame.audio.channels.set(2)


news_source_active = ref(false)
news_final_source_amplify = ref(0.0)


sse_publisher_url = environment.get(
  "SSE_PUBLISHER_URL", 
  default="https://openbroadcast.ch/sse/"
)

sse_publisher_api_token = environment.get(
  "SSE_PUBLISHER_API_TOKEN", 
  default=""
)

harbor_port = int_of_string(environment.get(
  "HARBOR_PORT",
  default="8000"
))

news_source = mksafe(input.http(
  "https://rfi.my/liveFRM96",
))

jingle_opener = "jingles/opener.mp3"
jingle_closer = "jingles/closer.mp3"


#######################################################################
# schedule
# NOTE: times in UTC
# durations for each hour, weekdays & weekends
#######################################################################
news_schedule = [
  ( 9, (600, 600)),
  (10, (600, 600)), # Tranche d'information 30' ?
  (11, (600, 600)), # Journal 10'
  (12, (600, 600)), # Journal 10'
  (13, (600, 600)), # Journal 10'
  (14, (600, 600)), # Journal 10'
  (15, (600, 600)), # Journal 10'
  (16, (600, 600)), # Journal 10'
  (17, (600, 600)), # Journal 10'
  (18, (600, 600)), # Journal 10'
  (19, (600, 600)), # Journal 10'
  (20, (600, 600)), # Journal 10'
]

print("schedule: #{news_schedule}");

#######################################################################
# jingle insertion queues
#######################################################################
news_source_queue = request.queue()
news_final_queue = request.queue()



#######################################################################
# handlers
#######################################################################
def sse_publish(cmd, payload = {})
  #<
  publish event to SSE publisher API
  >#

  print("SSE: #{cmd} - #{payload}");

  uri = "#{sse_publisher_url}news/"
  print("POST: #{uri}")
  h = http.post(
    headers=[
      ("Content-Type", "application/json; charset=UTF-8"),
      ("User-Agent", "News-Stream/0.0.1"),
      ("Authorization", "Bearer #{sse_publisher_api_token}"),
    ],
    timeout=5.0,
    data=json.stringify({
      cmd=cmd,
      ...payload
    }),
    uri
  )
  if h.status_code == 201 then
    print("SSE OK: #{cmd} - #{h}")
  else
    print("SSE ERROR: failed to publish event: #{h.status_code} - #{h}")
  end

end


def news_end()

  print("news:end");

  thread.run(
    #################################################################
    delay=1.0,
    #################################################################
    fun() -> begin
      print("final-queue: start closer");
      news_final_queue.push(
        request.create(jingle_closer)
      );
    end
  )

  thread.run(
    #################################################################
    delay=1.0,
    #################################################################
    fun() -> begin
      print("final-queue: set amplify to 0.0");
      news_final_source_amplify.set(0.0);
    end
  )

  # "scheduled" steps
  thread.run(
    #################################################################
    delay=7.0,
    #################################################################
    fun() -> begin
      sse_publish(
        "stop",
        {
          ts=time(),
          provider="rfi"
        }
      );
    end
  )

end

def news_begin(duration)

  print("news:begin: #{duration}s");

  thread.run(
    #################################################################
    delay=2.0,
    #################################################################
    fun() -> begin
      print("final-queue: set amplify to 1.0");
      news_final_source_amplify.set(1.0);
    end
  )

  thread.run(
    #################################################################
    delay=4.0,
    #################################################################
    fun() -> begin
      print("final-queue: start opener");
      news_final_queue.push(
        request.create(jingle_opener)    
      );
    end
  )

  # "scheduled" steps
  thread.run(
    #################################################################
    delay=4.0,
    #################################################################
    fun() -> begin
      sse_publish(
        "start",
        {
          ts=time(),
          provider="rfi"
        }
      );
    end
  )

  # schedule end of news
  thread.run(
    #################################################################
    delay=duration + 5.0 + 5.0 - 2.0,
    #################################################################
    fun() -> begin
      news_end();
    end
  )

end




#######################################################################
# HTTP server
#######################################################################
harbor.http.register.simple(
  port=harbor_port,
  method="POST",
  "/news-begin",
  fun(r) -> begin
    let json.parse ({
      duration,
    } : {
      duration: float,
    }) = r.data()

    news_begin(duration)

    http.response(
      content_type="text/plain",
      data="OK",
    )
  end
)


#######################################################################
# News scheduling
#######################################################################
def get_news_duration_for_time(t) =
  t_utc = time.utc(t)

  x = list.assoc(
    default=(0, 0),
    t_utc.hour,
    news_schedule
  )
  if t_utc.week_day <= 5 then
    fst(x)
  else
    snd(x)
  end
end


thread.when(
  # runs every hour at 0 minutes
  predicate.activates(
    { 0m }
  ), 
  fun() -> begin
    duration = get_news_duration_for_time(time())
    if duration > 0 then
      print("ND: #{duration}")
      news_begin(float_of_int(duration))
    end
  end
)


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
# DEV / output
#######################################################################

# output(news_final)

#######################################################################
# HLS / output
#######################################################################


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

output.harbor.hls(
  port=harbor_port,
  playlist="rfi.m3u8",
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
#   "/Users/ohrstrom/code/obr-web/playground/news/rfi/hls",
#   playlist="rfi.m3u8",
#   segment_duration=1.0,
#   segments=5,
#   segments_overhead=5,
#   segment_name=hls_segment_name,
#   [
#     (
#       "aac_96",
#       %ffmpeg(
#         format="mpegts",
#         %audio(
#           channels=2,
#           samplerate=44100,
#           codec="aac",
#           b="96k",
#           profile="aac_low"
#         )
#       )
#     ),
#   ],
#   news_final
# )


# output(news_source)
# output(news_final)