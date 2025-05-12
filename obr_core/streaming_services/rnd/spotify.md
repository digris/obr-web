# Spotify

## Sync User Favorites


```python
import requests
from account.models import User
from catalog.models import Media

user = User.objects.get(email="none@none.no")
sa = user.social_auth.filter(provider="spotify").first()


url = "https://api.spotify.com"

headers = {
    "Authorization": f"Bearer {access_token}",
}


me_url = url + "/v1/me"

me_url = url + "/v1/me/top/tracks?time_range=long_term"


r = requests.get(me_url, headers=headers)

user_id = "314jgc62dpsapatbo5t3oh63kbna"

playlist_url = url + f"/v1/users/{user_id}/playlists"



# tracks_url = url + "/tracks"

pl = {
    "name": "foo bar",
    "public": False,
}

```