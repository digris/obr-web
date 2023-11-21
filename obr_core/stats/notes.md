https://www.agiliq.com/blog/2017/12/django-20-window-expressions-tutorial/

```python
from django.db.models import Avg, F, Window, Sum, Q, Count, WindowFrame
from django.db.models.functions import  Rank, DenseRank, CumeDist, TruncHour, ExtractHour
from django.db.models.functions import Lag, Lead
from django.db.models import Value
from stats.models import PlayerEvent



qs = PlayerEvent.objects.annotate(
    time_end=Window(
        expression=Lead('time'),
        partition_by=[F("user_identity"), F("device_key")],
        order_by=F("time").asc()
    ),
    duration=F('time_end') - F('time'),
)

qs2 = PlayerEvent.objects.annotate(
    time_end=Window(
        expression=Lag('time'),
        order_by=F("time").desc()
    ),
    duration=F('time_end') - F('time'),
)

qs.aggregate(
    paused=Sum('duration', filter=Q(state='paused')),
    playing=Sum('duration', filter=Q(state='playing')),
)



qs = PlayerEvent.objects.annotate(
    time_end=Window(
        expression=Lead('time'),
        partition_by=[F("user_identity"), F("device_key")],
        order_by=F("time").asc()
    ),
    duration=F('time_end') - F('time'),
    hour=TruncHour('time'),
)


qs.annotate(
    hour=TruncHour('time')
).values('hour').annotate(
    c=Count('id'),
    playing=Sum('duration', filter=Q(state='playing')),
).values('hour', 'playing')


def print_qs(qs):
    for e in qs:
        if not e.time_end:
            continue
        print(f'{e.state}\t{e.obj_key} {e.user_identity}  {e.time:%H:%M:%S} - {e.time_end:%H:%M:%S}  :  {e.duration}')

        
      
      
      
      
      
from catalog.models import Media
durations = dict(Media.objects.values_list('uid', 'duration'))  

        
def print_qs(qs):
    for e in qs:
        if not e.time_end:
            continue
        print(f'{e.state}\t{e.obj_key} {e.user_identity}  {e.time:%H:%M:%S} - {e.time_end:%H:%M:%S}  :  {e.duration} /  {durations[e.obj_key[-8:]]}')
        
        
        
for e in PlayerEvent.objects.annotate(next=Window(expression=Lag('time'), order_by=F("time").desc())):
    if not e.next:
        continue
    print(f'{e.state}\t{e.obj_key} {e.user_identity} {e.time:%H:%M:%S} - {e.next:%H:%M:%S}  :  {e.next - e.time} ')
```
    