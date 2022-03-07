```python
from catalog.models.media import Media, Airplay
from catalog.models.playlist import Playlist
from broadcast.models import Emission
from django.db.models.functions import Now

Media.objects.count()
Airplay.objects.count()

qs = Media.objects.all()

for m in qs:
    ids = list(m.airplays.filter(time_end__lte=Now()).order_by('-time_end').values_list('id', flat=True)[1:])
    print(ids)
    Airplay.objects.filter(id__in=ids).delete()
    
Airplay.objects.count()


qs = Playlist.objects.all()

delete_ids = []
for p in qs:
    delete_ids += list(p.emissions.filter(time_end__lte=Now()).order_by('-time_end').values_list('id', flat=True)[1:])
    # print(ids)
    # Emission.objects.filter(id__in=ids).delete()
    
print(len(delete_ids))

```