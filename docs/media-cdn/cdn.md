# CDN (GCP)

## Protected Media Files (= encoded Audio)

- Media files are served from a bucket (`obr-media`) via CDN.
- Access is limited authenticated `Users` (having a valid `Subscription`)
- Authorization is implemented via signed cookie `Cloud-CDN-Cookie`


### "Webiste-Mode"

In "website-mode" (=consuming the app via browser) setting & removing the cookie is implemented in the session handling.


### "App-Mode" (iOS)

In "app-mode" the API and other resources are accessed in a state-less / session-less way, providing a JWT 
`accessToken` in the header of every request.

NOTE: see [docs/api/account](../api/account.md) for details.

The `cdnPolicy` required for CDN-access is included in the user endpoint:  

```
# `/api/v1/account/users/me/`

{
  ...
  "cdnPolicy": "URLPrefix=...:Expires=1979474012:KeyName=cdn-key:Signature=..."
  ...
}
```


### Media File URL Patterns

Media items (a.k.a. "Tracks") can be mapped directly to CDN resources via `UID`:

```
e.g.: 
https://next.openbroadcast.ch/discover/tracks/57E76303/
#
https://next.openbroadcast.ch/discover/tracks/<-UID-->/
```

can be mapped to:

```
https://<media-endpoint>/encoded/<uid>/<hls|dash>/manifest.<mpd|m3u8>
```

for `DASH` the example form above would result in:

```
https://media.next.openbroadcast.ch/encoded/57E76303/dash/manifest.mpd
```

and accordingly for `HLS`:

```
https://media.next.openbroadcast.ch/encoded/57E76303/hls/manifest.m3u8
```


### Test File

For testing implementations the following URL / file can be used:

```
https://media.next.openbroadcast.ch/encoded/0000TEST/test-credentials.txt
```


### Example Scripts

#### User Details

```python
# get user / cdn_policy
import requests
from getpass import getpass

def get_user():
    email = "api-test@openbroadcast.ch"
    password = getpass("password: ")
    url = "https://next.openbroadcast.ch/api/v1/account/login/"
    r = requests.post(url, json={"email": email, "password": password})
    return r.json()

user = get_user()
cdn_policy = user["cdnPolicy"]
```

#### CDN request using `urllib`

```python
from urllib.request import urlopen, Request

test_url = "https://media.next.openbroadcast.ch/encoded/0000TEST/test-credentials.txt"

# should fail
urlopen(Request(test_url)).read()

# should succeed
urlopen(Request(test_url, headers={"Cookie": f"Cloud-CDN-Cookie={cdn_policy}"})).read()
```

#### CDN request using `requests`

```python
import requests

test_url = "https://media.next.openbroadcast.ch/encoded/0000TEST/test-credentials.txt"

requests.get(test_url)  # <Response [403]>

requests.get(test_url, cookies={"Cloud-CDN-Cookie": cdn_policy})  # <Response [200]>
```


#### CDN request using `curl`

```shell
TEST_URL="https://media.next.openbroadcast.ch/encoded/0000TEST/test-credentials.txt"
CDN_POLICY="..."

curl \
  -b "Cloud-CDN-Cookie=${CDN_POLICY}" \
  $TEST_URL

```