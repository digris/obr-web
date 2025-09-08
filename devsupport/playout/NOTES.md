# Playout / Streaming Notes

## Audio Levels EBU R 128

```shell
export FILTER="[0:a]ebur128=video=1:meter=18:gauge=1[v]"
```

### DAB

```shell
nc edi-ch.digris.net 8857 | \
  dablin -w -s 0x4DA4 -f edi /dev/stdin | \
  ffmpeg -hide_banner \
  -i - \
  -filter_complex "$FILTER" \
  -map "[v]" -map 0:a -c:v libx264 -c:a aac -f mpegts - | \
  ffplay -window_title "DAB+ EBU R 128" -i -
```

### Stream

```shell
ffmpeg -hide_banner \
  -i 'http://stream.openbroadcast.ch/320.mp3' \
  -filter_complex "$FILTER" \
  -map "[v]" -map 0:a -c:v libx264 -c:a aac -f mpegts - | \
  ffplay -window_title "Stream EBU R 128" -i -
```

### Chain

```shell

# playout
export SRC=http://46.101.248.105/main.mp3

# ingress
-

# egress
export SRC=http://172.30.193.12:8001/egress.wav


ffmpeg -hide_banner \
  -i ${SRC} \
  -filter_complex "$FILTER" \
  -map "[v]" -map 0:a -c:v libx264 -c:a aac -f mpegts - | \
  ffplay -window_title "${SRC}" -i -
```