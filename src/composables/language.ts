import { computed } from "vue";
import { useCookies } from "@vueuse/integrations/useCookies";

const COOKIE_NAME = "language";

const useLanguage = () => {
  const cookies = useCookies([COOKIE_NAME], { autoUpdateDependencies: true });
  const currentLanguage = computed(() => {
    return cookies.get(COOKIE_NAME);
  });
  const setLanguage = (value: string) => {
    cookies.set(COOKIE_NAME, value, { path: "/" });
    // @ts-ignore
    window.i18n.global.locale = value;
  };
  return {
    currentLanguage,
    setLanguage,
  };
};

export { useLanguage };
