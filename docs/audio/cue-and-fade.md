# Audio Playback


## Example

NOTE: in general the API uses seconds for duration based values.

### API Resource

```text
{
    "results": [
        {
            "ct": "catalog.media",
            ...
            "duration": 300,
            "fadeIn": 5,
            "fadeOut": 5,
            "cueIn": 10,
            "cueOut": 10,
            ...
```

### Playback Behaviour

![fade and queue](../diagrams/audio/cue-and-fade.drawio.svg)


## Development Playlist

- Playlist UID: `80FB3498`
- [Web](https://next.openbroadcast.ch/discover/playlists/80FB3498/)
- [API](https://next.openbroadcast.ch/api/v1/catalog/media/?limit=16&offset=0&ordering=&obj_key=catalog.playlist:80FB3498)

| UID       | title          | dur. [s] |  cue-in [s] |  cue-out [s] | fade-in [s] |  fade-out [s] | play dur. [s] |
|-----------|----------------|---------:|------------:|-------------:|------------:|--------------:|--------------:|
| 744047E7  | Gold           |      285 |          10 |           95 |           5 |             5 |           180 |
| 481D8C39	 | The Heat       |      196 |          10 |            6 |           5 |             5 |           180 |
| 0149AB3C	 | All I Need     |      268 |          28 |            0 |          10 |            10 |           240 |
| 33C1A374  | Melt           |      250 |           0 |           10 |          10 |            10 |           240 |
| D09A9B23	 | Limit To ...   |      280 |           5 |            5 |          20 |            20 |           270 |
| 21C96F36  | Lucky I Got .. |      256 |           0 |           16 |          20 |            20 |           240 |
| 4626AD86  | Minitoka       |      564 |          10 |           14 |          30 |            30 |           540 |
| 24EF18C5  | Ajele          |     7204 |        3600 |         3304 |          10 |            10 |           300 |
| 57909A3A  | Man in a ...   |      207 |          20 |            7 |          30 |            30 |           180 |