interface AudioAnalyser {
  a32: AnalyserNode;
  a1024: AnalyserNode;
}

const createAudioAnalyser = (audio: HTMLAudioElement): AudioAnalyser => {
  const context = new AudioContext();
  const source = context.createMediaElementSource(audio);

  const a32 = context.createAnalyser();
  a32.smoothingTimeConstant = 0.9;
  a32.fftSize = 32;
  a32.minDecibels = -80;
  a32.maxDecibels = -5;
  source.connect(a32);

  const a1024 = context.createAnalyser();
  a1024.smoothingTimeConstant = 0.95;
  a1024.fftSize = 1024;
  source.connect(a1024);

  source.connect(context.destination);

  return {
    a32: a32,
    a1024: a1024,
  };
};

export type { AudioAnalyser };
export { createAudioAnalyser };
