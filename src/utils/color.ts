const getContrastColor = (rgb: Array<number>) => {
  const mean = rgb.reduce((s, b) => s + b, 0) / 3;
  return (mean > 64) ? [0, 0, 0] : [255, 255, 255];
};

// eslint-disable-next-line import/prefer-default-export
export { getContrastColor };
