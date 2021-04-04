// import eventBus from '@/eventBus';
import store from '@/store';

// import EventBus from '../eventBus';

// const SCROLL_UPDATE_THROTTLE = 10;

const getContrastColor = (color) => {
  const rgb = color.split(',').map((s) => parseInt(s, 10));
  const mean = rgb.reduce((s, b) => s + b, 0) / 3;
  console.debug('rgb', rgb, mean);
  return (mean > 128) ? '0, 0, 0' : '255, 255, 255';
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
