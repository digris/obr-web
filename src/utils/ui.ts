import settings from "@/settings";
import { watchDebounced } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { useUiStore } from "@/stores/ui";
import { getContrastColor } from "@/utils/color";

const setDocumentPrimaryColor = (color: Array<number>) => {
  const bg = color;
  const fg = getContrastColor(bg);
  const fgInverse = getContrastColor(fg);
  const { style } = document.body;
  style.setProperty("--c-live-bg", bg.join(","));
  style.setProperty("--c-live-fg", fg.join(","));
  style.setProperty("--c-live-fg-inverse", fgInverse.join(","));
};

class UIStateHandler {
  constructor() {
    // set initial color (passed via django template / settings)
    const color = settings.COLOR;
    if (color) {
      setDocumentPrimaryColor(color);
    }
    const { primaryColor } = storeToRefs(useUiStore());
    // watch(() => primaryColor.value, setDocumentPrimaryColor);
    watchDebounced(primaryColor, setDocumentPrimaryColor, { debounce: 200 });
  }
}

export default function () {
  return new UIStateHandler();
}
