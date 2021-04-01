import subprocess


def encode_dash(src, dst):
    print(f"encode_dash: {src} - {dst}")
    print(subprocess.check_output("ffmpeg -version", shell=True).decode("utf-8"))
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-v 32",
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

    print(" ".join(cmd))

    out = subprocess.check_output(" ".join(cmd), shell=True).decode("utf-8")

    print(out)
