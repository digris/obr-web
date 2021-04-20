import base64
import certifi
import json
import urllib3


BRIDGE_ENDPOINT = "https://next.openbroadcast.ch/api/v1/pub-sub-bridge/"
API_TOKEN = "e81c751013a0667fe43f7ed445e3160320107906"


def post_payload(payload):
    url = BRIDGE_ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {API_TOKEN}",  # Note: DRF style
    }
    body = json.dumps(payload).encode("utf-8")
    http = urllib3.PoolManager(ca_certs=certifi.where())
    r = http.request("POST", url=url, body=body, headers=headers)
    try:
        return json.loads(r.data.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        return r.data.decode("utf-8")


def bridge(event, context):

    if "data" not in event:
        print("payload missing")

    decoded = base64.b64decode(event["data"]).decode("utf-8")
    payload = json.loads(decoded)

    print("payload:", payload)

    result = post_payload(payload)

    print("result:", result)
