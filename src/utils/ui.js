// import eventBus from '@/eventBus';
import store from '@/store';

// import EventBus from '../eventBus';

// const SCROLL_UPDATE_THROTTLE = 10;

const getContrastColor = (color) => {
  const rgb = color.split(',').map((s) => parseInt(s, 10));
  console.debug('rgb', rgb);
  return color;
};

class UIStateHandler {
  constructor() {
    console.debug('UIStateHandler');
    // store.dispatch('ui/setViewport', { viewport });
    store.watch((state) => state.ui.colors, (newColors) => {
      const { bg } = newColors;
      const fg = getContrastColor(bg);
      console.debug('bg:', bg, 'fg:', fg);
      document.body.style.setProperty('--c-live-bg', bg);
      document.body.style.setProperty('--c-live-fg', fg);
    });
  }
}

// store.watch((state) => state.ui.scrollY, (n, o) => {
//   console.debug('n / o', n, o);
// });

export default new UIStateHandler();
