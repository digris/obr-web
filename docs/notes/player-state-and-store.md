# Player State & Store

## Initial State

```javascript
playerState = {
    isLive: false,
    isStopped: true,
    isBuffering: false,
    isPlaying: false,
    isPaused: true,
    duration: null,
    bandwidth: 0,
    currentTime: 0,
    relPosition: null,
    playheadTime: null,
}
```

## Playing State

### On-Demand

```javascript
playerState = {
    isLive: false,
    isStopped: true,
    isBuffering: false,
    isPlaying: true,
    isPaused: false,
    duration: 279.9,
    bandwidth: 256000,
    currentTime: 22.55008,
    relPosition: 0.0805647731332619,
    playheadTime: null
}
```

### Live

```javascript
playerState = {
    isLive: true,
    isStopped: true,
    isBuffering: false,
    isPlaying: true,
    isPaused: false,
    duration: null,
    bandwidth: 563200,
    currentTime: DateTime,
    relPosition: null,
    playheadTime: DateTime
}
```