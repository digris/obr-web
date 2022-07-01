interface AudioAnalyser {
  a64: AnalyserNode;
  a1024: AnalyserNode;
}

const createAudioAnalyser = (audio: HTMLAudioElement) => {
  const context = new AudioContext();
  const source = context.createMediaElementSource(audio);

  const a64 = context.createAnalyser();
  const a1024 = context.createAnalyser();

  a64.smoothingTimeConstant = 0.8;
  a1024.smoothingTimeConstant = 0.95;

  a64.fftSize = 64;
  a1024.fftSize = 1024;

  source.connect(a64);
  source.connect(a1024);

  source.connect(context.destination);

  return {
    a64: a64,
    a1024: a1024,
  };
};

export type { AudioAnalyser };
export { createAudioAnalyser };
