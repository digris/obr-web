#! /usr/bin/env liquidsoap

settings.log.stdout.set(true)
settings.log.level.set(2)
settings.log.unix_timestamps.set(false)

settings.frame.audio.samplerate.set(44100)
settings.frame.audio.channels.set(2)

news_source_active = ref(false)

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

output(news_source)
# output(news_final)