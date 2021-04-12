import os
import tempfile
from pathlib import Path
from flask import Flask, request
from google.cloud import storage
import encoder


VERSION = "0.0.1"

SRC_BUCKET = "obr-master"
DST_BUCKET = "obr-media"


app = Flask(__name__)


def download_file(bucketname, path, workdir, filename):

    print(f"download_file {bucketname}/{path} to {workdir}:{filename}")

    client = storage.Client()
    bucket = client.bucket(bucketname)
    blob = bucket.blob(path)
    local_file = os.path.join(workdir, filename)

    blob.download_to_filename(local_file)

    return local_file


def upload_dir(src, bucketname, path):

    print(f"upload_dir {src} to {bucketname}/{path}")

    client = storage.Client()
    bucket = client.bucket(bucketname)

    for f in Path(src).iterdir():
        if f.is_file():
            blob = bucket.blob(os.path.join(path, f.name))
            blob.upload_from_filename(f)


@app.route("/", methods=["GET"])
def index():
    return f"OBR Media Encoder - v{VERSION}", 200


@app.route("/encode-dash", methods=["POST"])
def encode_dash():
    # The ce-Resourcename value will be something like this: projects/_/buckets/sayle-eventarc/objects/test_file.txt
    authorization = request.headers.get("Authorization")
    payload = request.get_json()
    path = payload.get("path")
    print(f"path: {path}")

    workdir = tempfile.mkdtemp()
    uid, filename = os.path.split(path)
    src = download_file(
        bucketname=SRC_BUCKET,
        path=path,
        workdir=workdir,
        filename=filename,
    )

    dst_dir = os.path.join(workdir, "dash")
    os.mkdir(dst_dir)
    dst = os.path.join(dst_dir, "manifest.mpd")

    encoder.encode_dash(src=src, dst=dst)

    upload_dir(src=dst_dir, bucketname=DST_BUCKET, path=f"encoded/{uid}/dash")

    return {"path": path}, 200


@app.route("/encode-hls", methods=["POST"])
def encode_hls():
    # The ce-Resourcename value will be something like this: projects/_/buckets/sayle-eventarc/objects/test_file.txt
    authorization = request.headers.get("Authorization")
    payload = request.get_json()
    path = payload.get("path")
    print(f"path: {path}")

    workdir = tempfile.mkdtemp()
    uid, filename = os.path.split(path)
    src = download_file(
        bucketname=SRC_BUCKET,
        path=path,
        workdir=workdir,
        filename=filename,
    )

    dst_dir = os.path.join(workdir, "hls")
    os.mkdir(dst_dir)
    dst = os.path.join(dst_dir, "manifest.m3u8")

    encoder.encode_hls(src=src, dst=dst)

    upload_dir(src=dst_dir, bucketname=DST_BUCKET, path=f"encoded/{uid}/hls")

    return {"path": path}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
