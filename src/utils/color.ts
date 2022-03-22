const CONTRAST_BREAKPOINT = 86;

const getMediaColor = (media: object) => {
  // @ts-ignore
  if (!(media.releases && media.releases.length)) {
    return null;
  }
  // @ts-ignore
  return media.releases[0].image?.rgb;
};

const getContrastColor = (rgb: Array<number>) => {
  const mean = rgb.reduce((s, b) => s + b, 0) / 3;
  return mean > CONTRAST_BREAKPOINT ? [0, 0, 0] : [255, 255, 255];
};

const setBodyColorTheme = (theme: string) => {
  const { body } = document;
  body.setAttribute("data-page-color", theme);
};

export { getMediaColor, getContrastColor, setBodyColorTheme };
