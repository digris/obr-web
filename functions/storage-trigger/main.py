import urllib3
import certifi
import json
import multiprocessing

ENCODER_ENDPOINT = "https://media-encoder-kcek2ea7xq-oa.a.run.app"
API_TOKEN = "N1ZOBHLZ9JL141VHAC7H"


def encode_format(path, encoding_format):
    print(f"encode: {path}")
    payload = {"path": path}
    url = f"{ENCODER_ENDPOINT}/encode-{encoding_format}"
    headers = {
        "Content-Type": "application/json",
        "Authentication": f"Bearer {API_TOKEN}",  # Note: Flask style
    }
    body = json.dumps(payload).encode("utf-8")
    http = urllib3.PoolManager(ca_certs=certifi.where())
    r = http.request("POST", url=url, body=body, headers=headers)
    data = json.loads(r.data.decode("utf-8"))
    return data


def created(event, context):

    print("Event ID: {}".format(context.event_id))
    print("Event type: {}".format(context.event_type))
    print("Bucket: {}".format(event["bucket"]))
    print("File: {}".format(event["name"]))
    print("Metageneration: {}".format(event["metageneration"]))
    print("Created: {}".format(event["timeCreated"]))
    print("Updated: {}".format(event["updated"]))

    print(json.dumps(event))

    if not context.event_type == "google.storage.object.finalize":
        print(f"invalid event type: {context.event_type}")
        return

    path = event["name"]

    p_dash = multiprocessing.Process(target=encode_format, args=[path, "dash"])
    p_hls = multiprocessing.Process(target=encode_format, args=[path, "hls"])

    p_dash.start()
    p_hls.start()

    p_dash.join()
    p_hls.join()

    # result = encode_format(path, "dash")
    # print(result)
    #
    # result = encode_format(path, "hls")
    # print(result)
