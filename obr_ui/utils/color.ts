const CONTRAST_BREAKPOINT = 86;

const getMediaColor = (media: any) => {
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

const getAppTheme = (rgb: Array<number>) => {
  const mean = rgb.reduce((s, b) => s + b, 0) / 3;
  return mean > CONTRAST_BREAKPOINT ? "dark" : "light";
};

const setBodyColorTheme = (theme: string) => {
  const { body } = document;
  body.setAttribute("data-page-theme", theme);
};

export { getAppTheme, getContrastColor, getMediaColor, setBodyColorTheme };
