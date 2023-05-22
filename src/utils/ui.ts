import { watchDebounced } from "@vueuse/core";
import { storeToRefs } from "pinia";

import settings from "@/settings";
import { useUiStore } from "@/stores/ui";
import { getAppTheme, getContrastColor } from "@/utils/color";

const setDocumentThemeColor = async (color: Array<number>) => {
  const el: HTMLMetaElement | null = document.getElementById("theme-color");
  if (el) {
    el.content = `rgb(${color.join(" ")})`;
  }
};

const setAppTheme = async (color: Array<number>) => {
  const theme = getAppTheme(color);
  await window.appBridge.send("ui:setTheme", { theme });
};

const setDocumentPrimaryColor = (color: Array<number>) => {
  const bg = color;
  const fg = getContrastColor(bg);
  const fgInverse = getContrastColor(fg);
  const { style } = document.body;
  // console.debug("colors", { bg, fg, fgInverse });
  style.setProperty("--c-live-bg", bg.join(" "));
  style.setProperty("--c-live-fg", fg.join(" "));
  style.setProperty("--c-live-fg-inverse", fgInverse.join(" "));
  setTimeout(async () => {
    await setDocumentThemeColor(color);
  }, 50);
  setTimeout(async () => {
    await setAppTheme(color);
  }, 50);
};

class UIStateHandler {
  constructor() {
    // set initial color (passed via django template / settings)
    const color = settings.COLOR;
    if (color) {
      setDocumentPrimaryColor(color);
      setDocumentThemeColor(color);
    }
    const { primaryColor } = storeToRefs(useUiStore());
    // watch(() => primaryColor.value, setDocumentPrimaryColor);
    watchDebounced(primaryColor, setDocumentPrimaryColor, { debounce: 200 });
  }
}

export default function () {
  return new UIStateHandler();
}
