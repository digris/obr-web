import store from '@/store';
import settings from '@/settings';
import { getContrastColor } from '@/utils/color';

const setTitle = (title: string) => {
  document.title = title;
};

const setPrimaryColor = (color: Array<number>) => {
  const bg = color;
  const fg = getContrastColor(bg);
  const fgInverse = getContrastColor(fg);
  const { style } = document.body;
  style.setProperty('--c-live-bg', bg.join(','));
  style.setProperty('--c-live-fg', fg.join(','));
  style.setProperty('--c-live-fg-inverse', fgInverse.join(','));
};

class UIStateHandler {
  constructor() {
    // set initial color (passed via django template / settings)
    const color = settings.COLOR;
    if (color) {
      setPrimaryColor(color);
    }
    // TODO: https://codeburst.io/vuex-and-typescript-3427ba78cfa8
    // implement types on store
    window.addEventListener('load', () => {
      this.updateViewport();
    });
    window.addEventListener('resize', () => {
      this.updateViewport();
    });
    store.watch((state: any) => state.ui.title, (title) => {
      setTitle(title);
    });
    store.watch((state: any) => state.ui.primaryColor, (newColor) => {
      setPrimaryColor(newColor);
    });
  }

  // eslint-disable-next-line class-methods-use-this
  async updateViewport() {
    const html = document.documentElement;
    const viewport = {
      left: window.scrollX,
      top: window.scrollY,
      width: window.innerWidth || html.clientWidth,
      height: window.innerHeight || html.clientHeight,
    };
    await store.dispatch('ui/setViewport', viewport);
  }
}

export default function () {
  return new UIStateHandler();
}
