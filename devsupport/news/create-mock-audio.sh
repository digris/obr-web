#! /bin/bash

rm -f mock/ref/*.wav

mkdir -p mock/ref && cd mock

# generate sine / silence files
sox -n -c 2 10s_-50dB.wav synth 10 sine 1000 vol -50dB

sox -n -c 2 3s_-30dB.wav synth 3 sine 1000 vol -30dB

sox -n -c 2 3s_silence.wav trim 0 3

sox -n -c 2 20s_silence.wav trim 0 20

sox -n -c 2 24s_-50dB.wav synth 24 sine 1000 vol -50dB

# extract 60s from example news file
ffmpeg -y -loglevel quiet -i ../recorded/recorded_stream.aac -t 60 -acodec pcm_s16le 60s_audio.wav

# combine files
sox 10s_-50dB.wav 3s_-30dB.wav 3s_silence.wav 60s_audio.wav 20s_silence.wav 24s_-50dB.wav ref/mock-news.wav

# cleanup
rm 10s_-50dB.wav 3s_-30dB.wav 3s_silence.wav 60s_audio.wav 20s_silence.wav 24s_-50dB.wav

cd ..
