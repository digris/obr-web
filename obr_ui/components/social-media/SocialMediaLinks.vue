<script type="ts">
import { computed, defineComponent } from 'vue';

import IconFacebook from "@/components/ui/icon/brand/IconFacebook.vue";
import IconGithub from "@/components/ui/icon/brand/IconGithub.vue";
import IconInstagram from "@/components/ui/icon/brand/IconInstagram.vue";

export default defineComponent({
  components: {
    IconInstagram,
    IconFacebook,
    IconGithub,
  },
  setup() {
    const links = computed(() => {
      return {
        instagram: "https://www.instagram.com/openbroadcastradio/",
        facebook: "https://www.facebook.com/OpenBroadcast/",
        github: "https://github.com/digris/obr-web",
      };
    });
    return {
      links,
    };
  },
});
</script>

<template>
  <div class="social-media-links">
    <div class="links">
      <a class="link link--instagram" target="_blank" :href="links.instagram">
        <IconInstagram :size="48" color="rgb(var(--c-light))" />
      </a>
      <a class="link link--facebook" target="_blank" :href="links.facebook">
        <IconFacebook :size="48" color="rgb(var(--c-light))" />
      </a>
      <a class="link link--github" target="_blank" :href="links.github">
        <IconGithub :size="48" color="rgb(var(--c-light))" />
      </a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.social-media-links {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;

  .links {
    display: flex;

    .link {
      height: 56px;
      width: 56px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 0.5rem;
      color: rgb(var(--c-light));
      background: rgb(var(--c-dark));
      border-radius: 28px;

      &:hover {
        background: rgb(var(--c-dark) / 75%);
      }
    }
  }
}
</style>
