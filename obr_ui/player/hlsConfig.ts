export const hlsBaseConfig = {
  maxBufferLength: 30,
  maxMaxBufferLength: 30,
  backBufferLength: 30,
  liveDurationInfinity: true,
  liveSyncDurationCount: 3,
  lowLatencyMode: true,
  // xhrSetup: (xhr: XMLHttpRequest, url: string) => {},
  abrBandWidthFactor: 0.5,
  abrBandWidthUpFactor: 0.3,
  manifestLoadPolicy: {
    default: {
      maxTimeToFirstByteMs: Infinity,
      maxLoadTimeMs: 20000,
      timeoutRetry: {
        maxNumRetry: 200,
        retryDelayMs: 0,
        maxRetryDelayMs: 0,
      },
      errorRetry: {
        maxNumRetry: 100,
        retryDelayMs: 1000,
        maxRetryDelayMs: 8000,
      },
    },
  },
  playlistLoadPolicy: {
    default: {
      maxTimeToFirstByteMs: 10000,
      maxLoadTimeMs: 20000,
      timeoutRetry: {
        maxNumRetry: 200,
        retryDelayMs: 0,
        maxRetryDelayMs: 0,
      },
      errorRetry: {
        maxNumRetry: 200,
        retryDelayMs: 1000,
        maxRetryDelayMs: 8000,
      },
    },
  },
};
