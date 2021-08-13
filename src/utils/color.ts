const CONTRAST_BREAKPOINT = 86;

const getContrastColor = (rgb: Array<number>) => {
  const mean = rgb.reduce((s, b) => s + b, 0) / 3;
  return (mean > CONTRAST_BREAKPOINT) ? [0, 0, 0] : [255, 255, 255];
};

const setBodyColorTheme = (theme: string) => {
  const { body } = document;
  body.setAttribute('data-page-color', theme);
};

export { getContrastColor, setBodyColorTheme };
