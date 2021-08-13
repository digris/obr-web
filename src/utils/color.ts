const getContrastColor = (rgb: Array<number>) => {
  const mean = rgb.reduce((s, b) => s + b, 0) / 3;
  return (mean > 86) ? [0, 0, 0] : [255, 255, 255];
};

const setBodyColorTheme = (theme: string) => {
  const { body } = document;
  console.debug('theme', theme, body);
  body.setAttribute('data-page-color', theme);
};

export { getContrastColor, setBodyColorTheme };
