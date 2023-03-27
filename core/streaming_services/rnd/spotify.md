# Spotify

## Sync User Favorites


```python
import requests
from account.models import User
from catalog.models import Media

user = User.objects.get(email="jonas+deezer@anorg.net")

sa = user.social_auth.filter(provider="spotify").first()


url = "https://api.spotify.com"

headers = {
    "Authorization": f"Bearer {access_token}",
}


me_url = url + "/v1/me"

me_url = url + "/v1/me/top/tracks?time_range=long_term"


r = requests.get(me_url, headers=headers)





# tracks_url = url + "/tracks"

```