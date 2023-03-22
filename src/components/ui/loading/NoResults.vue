<script lang="ts">
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

export default defineComponent({
  props: {
    filter: {
      type: Object,
      default: () => {},
    },
  },
  setup(props) {
    const { t } = useI18n();
    const hasFilter = computed(() => {
      if (props.filter.q) {
        return true;
      }
      return !!props.filter.tags.length;
    });
    return {
      t,
      hasFilter,
    };
  },
});
</script>
<template>
  <div class="no-results">
    <slot name="default">
      <div v-if="hasFilter" class="body body--no-results">
        <i18n-t keypath="loading.noResults.lead" tag="p" />
        <i18n-t keypath="loading.noResults.cta" tag="p">
          <router-link to="" v-text="t('loading.noResults.ctaText')" />
        </i18n-t>
      </div>
      <div v-else class="body body--no-favorites">
        <i18n-t keypath="loading.noFavorites.lead" tag="p" />
        <i18n-t keypath="loading.noFavorites.cta" tag="p">
          <router-link to="/discover/" v-text="t('loading.noFavorites.ctaText')" />
        </i18n-t>
      </div>
    </slot>
  </div>
</template>
<style lang="scss" scoped>
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 4rem;
  margin-top: 4rem;
  margin-bottom: 4rem;

  > .body {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: var(--t-fs-large);

    a {
      text-decoration: underline;
    }
  }
}
</style>
