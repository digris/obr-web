# Media & Playback

- [API Doc - MediaList](http://local.obr-next:8080/api/v1/schema/redoc/#tag/catalog/operation/catalogMediaList)

## API Media (a.k.a. "Tracks") Endpoint

- `https://next.openbroadcast.ch/de/api/v1/catalog/media/`

### Expandable Fields

- `identifiers`, `image`, `tags`

### Selective Serialization

In case only a subset of fields is needed they can be selected using the `fields` parameter.  
The parameter can be comma-separated: `fields=uid,name` or repeated: `fields[]=uid&fields[]=name`

Complementary it is possible to exclude specific fields using the `omit` parameter.
The parameter can be comma-separated: `omit=artists,releases` or repeated: `omit[]=artists&omit[]=releases`

### Limits

As default listings are limited to 100 results. This can be changed using the `limit` parameter.

### Example Media Listing

```text
https://next.openbroadcast.ch/api/v1/catalog/media/
```

```json
{
    "count": 17341,
    "next": "https://next.openbroadcast.ch/api/v1/catalog/media/?limit=100&offset=100",
    "previous": null,
    "results": [
        {
            "ct": "catalog.media",
            "uid": "79979982",
            "url": "https://next.openbroadcast.ch/api/v1/catalog/media/79979982/",
            "name": "Swimmers",
            "artistDisplay": "Zero 7, Jem Cooke",
            "artists": [
                {
                    "url": "https://next.openbroadcast.ch/api/v1/catalog/artists/47A045B9/",
                    "ct": "catalog.artist",
                    "uid": "47A045B9",
                    "name": "Zero 7",
                    "joinPhrase": null
                },
                {
                    "url": "https://next.openbroadcast.ch/api/v1/catalog/artists/69B33661/",
                    "ct": "catalog.artist",
                    "uid": "69B33661",
                    "name": "Jem Cooke",
                    "joinPhrase": "feat"
                }
            ],
            "releases": [
                {
                    "ct": "catalog.release",
                    "uid": "10B894B9",
                    "url": "https://next.openbroadcast.ch/api/v1/catalog/releases/10B894B9/",
                    "name": "Swimmers",
                    "numMedia": 1,
                    "isNew": false,
                    "image": {
                        "ct": "catalog.releaseimage",
                        "uid": "556CE33C",
                        "path": "catalog/release/556CE33C/61322881.jpg",
                        "url": "https://storage.googleapis.com/ch-openbroadcast-media/catalog/release/556CE33C/61322881.jpg",
                        "ratio": 1,
                        "rgb": [
                            36,
                            91,
                            169
                        ]
                    }
                }
            ],
            "duration": 237,
            "latestAirplay": "2022-12-16T13:40:55.267075+01:00",
            "numAirplays": 4,
            "userRating": 1,
            "fadeIn": 0,
            "fadeOut": 0,
            "cueIn": 0,
            "cueOut": 0
        },
        ...
    ]
}
```


### Get Media for Object (e.g. Playlist, Mood, Artist)

The Media Endpoint can be used to only retrieve tracks "belonging" to a specific object.  
These results can e.g. be used to display "detail pages" or to feed the player / queue.


#### Example: Get Media for a Playlist

Given a playlist resource (e.g. retrieved from `/api/v1/catalog/playlists/`, `/api/v1/broadcast/program/` 
or `/api/v1/broadcast/schedule/`):


```json
{
  "ct": "catalog.playlist",
  "uid": "80FB3498",
  "url": "https://next.openbroadcast.ch/api/v1/catalog/playlists/80FB3498/",
  "name": "DEV - FADE / CUE",
  "image": {
    ...
  }
}
```

##### Object Key `obj_key`

Out of the resource the `obj_key` can be created using `ct` and `uid` (format: `<ct>:<uid>`)

In the case from above: `obj_key=catalog.playlist:80FB3498`

##### Filtered Media List

Using the `obj_key` the tracks for the given playlist can be retrieved:

```text
https://next.openbroadcast.ch/api/v1/catalog/media/?obj_key=catalog.playlist:80FB3498
```


#### Example: Get Media for a Mood

Given a playlist resource (e.g. retrieved from `/api/v1/catalog/moods/`):


```json
{
  "ct": "catalog.mood",
  "uid": "66BB2601",
  "url": "https://next.openbroadcast.ch/api/v1/catalog/moods/66BB2601/",
  "name": "Cocktail",
  "teaser": "Anything with friends around the table",
  "tags": [
    {
      "ct": "tagging.tag",
      "uid": "353C1BD8",
      "type": "activity",
      "name": "Cocktail"
    }
  ],
  "rgb": [119, 231, 199],
  ...
}
```

##### Object Key `obj_key`

Out of the resource the `obj_key` can be created using `ct` and `uid` (format: `<ct>:<uid>`)

In the case from above: `obj_key=catalog.mood:66BB2601`

##### Filtered Media List

Using the `obj_key` the tracks for the given mood can be retrieved:

```text
https://next.openbroadcast.ch/api/v1/catalog/media/?obj_key=catalog.mood:66BB2601
```