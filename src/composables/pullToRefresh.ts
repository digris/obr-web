import type { Ref } from "vue";
import { onActivated, onDeactivated } from "vue";
import { useI18n } from "vue-i18n";
import { useStyleTag } from "@vueuse/core";
import PullToRefresh from "pulltorefreshjs";

const STYLE = `
  .ptr--ptr {
    font-size: 1rem;
    font-weight: 400;
    color: rgba(0, 0, 0, 1);
    box-shadow: unset;
  }
  .ptr--box {
    padding: 20px 10px 11px;
    background: rgba(var(--c-black), 0.05);
    margin-bottom: 0.625rem;
  }
  .ptr--icon {
    color: inherit;
    font-size: 24px;
    transition: unset;
  }
  .ptr--text {
    color: inherit;
  }
`;

export function usePullToRefresh(rootEl: Ref<HTMLElement | null>, handler: () => any) {
  const { t } = useI18n();
  const { load: loadStyle, unload: unloadStyle } = useStyleTag(STYLE);
  onActivated(() => {
    console.debug("style loaded");
    if (!rootEl.value) {
      return;
    }
    loadStyle();
    PullToRefresh.init({
      // @ts-ignore
      mainElement: rootEl.value,
      onRefresh: handler,
      instructionsPullToRefresh: t("pullToRefresh.pull"),
      instructionsReleaseToRefresh: t("pullToRefresh.release"),
      instructionsRefreshing: t("pullToRefresh.refreshing"),
      // iconArrow: "&#8616;",
    });
  });
  onDeactivated(() => {
    if (!rootEl.value) {
      return;
    }
    PullToRefresh.destroyAll();
    unloadStyle();
  });
  return {};
}
