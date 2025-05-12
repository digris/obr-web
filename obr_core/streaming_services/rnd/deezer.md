# Deezer

## Sync User Favorites


```python
import requests
from account.models import User
from catalog.models import Media

user = User.objects.get(email="none@none.no")

sa = user.social_auth.filter(provider="deezer").first()


url = "https://api.deezer.com/user/me"

params = {
    "access_token": sa.access_token,
}


tracks_url = url + "/tracks"

tracks = []
while tracks_url:
    r = requests.get(tracks_url, params=params)
    result = r.json()
    tracks_url = result.get("next")
    for track in result["data"]:
        tracks.append(track)
    
m_tracks = [{"name": t["title"], "artist": t["artist"]["name"]} for t in tracks]


qs = Media.objects.using("sync").all()
qs = Media.objects.using("default").all()

media_ids = []
for t in m_tracks:
    m_qs = qs.filter(name=t["name"], artists__name=t["artist"])
    # if c := m_qs.count():
    #     print(c)
    if m := m_qs.first():
        print(m.uid, m)
        media_ids.append(m.id)

```

```python
from django.contrib.contenttypes.models import ContentType
from rating.models import Vote, VoteScope, VoteSource

votes_to_create = []
for obj in Media.objects.filter(id__in=media_ids):
    content_type = ContentType.objects.get_for_model(obj)
    try:
        vote = Vote.objects.get(
            user=user,
            content_type=content_type,
            object_id=obj.id,
        )
    except Vote.DoesNotExist:
        vote = Vote(
            user=user,
            source=VoteSource.ON_DEMAND,
            scope=VoteScope.UNDEFINED,
            value=1,
            content_type=content_type,
            object_id=obj.id,
        )
        votes_to_create.append(vote)
    
    

```