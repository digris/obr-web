import type { Ref } from "vue";
import { onActivated, onDeactivated } from "vue";
import { useI18n } from "vue-i18n";
import PullToRefresh from "pulltorefreshjs";

export function usePullToRefresh(rootEl: Ref<HTMLElement | null>, handler: () => any) {
  const { t } = useI18n();
  onActivated(() => {
    if (!rootEl.value) {
      return;
    }
    PullToRefresh.init({
      // @ts-ignore
      mainElement: rootEl.value,
      onRefresh: handler,
      instructionsPullToRefresh: t("pullToRefresh.pull"),
      instructionsReleaseToRefresh: t("pullToRefresh.release"),
      instructionsRefreshing: t("pullToRefresh.refreshing"),
      // iconArrow: "&#8616;",
      getStyles: () => "",
    });
  });
  onDeactivated(() => {
    if (!rootEl.value) {
      return;
    }
    PullToRefresh.destroyAll();
  });
  return {};
}
