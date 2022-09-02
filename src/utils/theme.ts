import { useSettingsStore } from "@/stores/settings";
import { storeToRefs } from "pinia";

const DATA_ATTRIBUTE = "data-theme";

export default function setDocumentTheme() {
  const { theme } = storeToRefs(useSettingsStore());
  if (theme.value) {
    document.body.setAttribute(DATA_ATTRIBUTE, theme.value);
  }
}
