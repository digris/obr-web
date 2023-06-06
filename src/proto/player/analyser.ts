interface AudioAnalyser {
  a1024: AnalyserNode;
}

const createAudioAnalyser = (audio: HTMLAudioElement): AudioAnalyser => {
  const context = new AudioContext();
  const source = context.createMediaElementSource(audio);

  const a1024 = context.createAnalyser();
  a1024.smoothingTimeConstant = 0.95;
  a1024.fftSize = 1024;

  source.connect(a1024);
  source.connect(context.destination);

  return {
    a1024: a1024,
  };
};

export type { AudioAnalyser };
export { createAudioAnalyser };
