import { useSettings } from "@/composables/settings";

const DATA_ATTRIBUTE = "data-theme";

export default function setDocumentTheme() {
  const { darkMode } = useSettings();
  const theme = darkMode.value ? "dark" : "light";
  document.body.setAttribute(DATA_ATTRIBUTE, theme);
}
