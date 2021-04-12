import store from '@/store';
// import { UIState } from '@/types';
import { getContrastColor } from '@/utils/color';

const setTitle = (title: string) => {
  document.title = title;
};

const setPrimaryColor = (color: Array<number>) => {
  const bg = color;
  const fg = getContrastColor(bg);
  const { style } = document.body;
  style.setProperty('--c-live-bg', bg.join(','));
  style.setProperty('--c-live-fg', fg.join(','));
};

class UIStateHandler {
  constructor() {
    // TODO: https://codeburst.io/vuex-and-typescript-3427ba78cfa8
    // implement types on store
    store.watch((state: any) => state.ui.title, (title) => {
      setTitle(title);
    });
    store.watch((state: any) => state.ui.primaryColor, (newColor) => {
      setPrimaryColor(newColor);
    });
  }
}

export default function () {
  return new UIStateHandler();
}
