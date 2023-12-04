import { toRef } from "vue";
import type { Ref } from "vue-demi";
import { useTitle } from "@vueuse/core";
import type { MaybeRefOrGetter } from "@vueuse/shared";

const TITLE_TEMPLATE = "%s | open broadcast radio";

const usePageTitle = (newTitle: MaybeRefOrGetter<string | null | undefined | unknown> = null) => {
  // @ts-ignore
  const title: Ref<string | null | undefined> = toRef(newTitle ?? document?.title ?? null);
  useTitle(title, { titleTemplate: TITLE_TEMPLATE });
  return { title };
};

export { usePageTitle };
