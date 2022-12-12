# Audio Playback


## Example

NOTE: in general the API uses seconds for duration based values.  
      with **the exception** of "intra-playback" related values (fades, cues) that base on milliseconds.

### API Resource

```text
{
    "results": [
        {
            "ct": "catalog.media",
            ...
            "duration": 300,
            "fadeIn": 5000,
            "fadeOut": 5000,
            "cueIn": 10000,
            "cueOut": 10000,
            ...
```

### Playback Behaviour

![fade and queue](../diagrams/audio/cue-and-fade.drawio.svg)


## Development Playlist

- Playlist UID: `80FB3498`
- [Web](https://next.openbroadcast.ch/discover/playlists/80FB3498/)
- [API](https://next.openbroadcast.ch/api/v1/catalog/playlists/80FB3498/?expand[]=media_set)

| UID       | title          | dur. [s] | cue-in [ms] | cue-out [ms] | fade-in [ms] | fade-out [ms] | play dur. [s] |
|-----------|----------------|---------:|------------:|-------------:|-------------:|--------------:|--------------:|
| 744047E7  | Gold           |      285 |       10000 |        95000 |         5000 |          5000 |           180 |
| 481D8C39	 | The Heat       |      196 |       10000 |         6000 |         5000 |          5000 |           180 |
| 0149AB3C	 | All I Need     |      268 |       28000 |            0 |        10000 |         10000 |           240 |
| 33C1A374  | Melt           |      250 |           0 |        10000 |        10000 |         10000 |           240 |
| D09A9B23	 | Limit To ...   |      280 |        5000 |         5000 |        20000 |         20000 |           270 |
| 21C96F36  | Lucky I Got .. |      256 |           0 |        16000 |        20000 |         20000 |           240 |
| 4626AD86  | Minitoka       |      564 |       10000 |        14000 |        30000 |         30000 |           540 |
| 24EF18C5  | Ajele          |     7204 |     3600000 |      3304000 |        10000 |         10000 |           300 |
| 57909A3A  | Man in a ...   |      207 |       20000 |         7000 |        30000 |         30000 |           180 |