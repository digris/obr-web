import os
import subprocess


def encode_dash(src, dst):
    print(f"encode_dash: {src} - {dst}")
    # print(subprocess.check_output("ffmpeg -version", shell=True).decode("utf-8"))
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel warning",
        "-i",
        src,
        "-ac 2",
        "-ar 44100",
        "-map 0:a -c:a:0 aac -b:a:0 64k",
        "-map 0:a -c:a:1 aac -b:a:1 256k",
        "-map_metadata -1",
        "-f dash",
        "-seg_duration 5",
        "-init_seg_name 'init-$RepresentationID$.m4s'",
        "-media_seg_name 'seg-$RepresentationID$-$Number%09d$.m4s'",
        "-adaptation_sets 'id=0,streams=a'",
        dst,
    ]

    # print(" ".join(cmd))
    out = subprocess.check_output(" ".join(cmd), shell=True).decode("utf-8")
    print(out)


def encode_hls(src, dst):
    print(f"encode_hls: {src} - {dst}")
    # print(subprocess.check_output("ffmpeg -version", shell=True).decode("utf-8"))

    dst_dir, dst_filename = os.path.split(dst)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel warning",
        "-i",
        src,
        "-ac 2",
        "-ar 44100",
        "-filter:a loudnorm",
        "-map 0:a -c:a:0 aac -b:a:0 64k",
        "-map 0:a -c:a:1 aac -b:a:1 256k",
        "-map_metadata -1",
        "-f hls",
        "-hls_time 5",
        "-hls_playlist_type vod",
        "-hls_flags independent_segments",
        "-hls_segment_type fmp4",
        f"-hls_segment_filename {dst_dir}/stream_%v-data%02d.ts",
        f"-master_pl_name {dst_filename}",
        f"-var_stream_map 'a:0 a:1' {dst_dir}/stream_%v.m3u8",
    ]

    print(" ".join(cmd))
    out = subprocess.check_output(" ".join(cmd), shell=True).decode("utf-8")
    print(out)
