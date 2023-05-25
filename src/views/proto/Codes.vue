<script lang="ts">
import { defineComponent } from "vue";
import QrcodeVue from "qrcode.vue";

import srcBadge from "@/assets/brand-icons/app-store.svg";

export default defineComponent({
  components: {
    QrcodeVue,
  },
  setup() {
    return {
      srcBadge,
    };
  },
});
</script>
<template>
  <div class="view">
    <div class="qr qr--store">
      <qrcode-vue
        value="https://itunes.apple.com/app/obr/id1643695398"
        size="512"
        background="#000000"
        foreground="#ffffff"
        level="H"
        render-as="svg"
      />
      <div
        class="badge"
      >
        <img :src="srcBadge" alt="" />
      </div>
      <div class="step">1</div>
    </div>
    <div class="qr qr--voucher">
      <qrcode-vue
        value="https://next.openbroadcast.ch/#KS-HM-ZH"
        size="512"
        background="#ffffff"
        foreground="#000000"
        level="H"
        render-as="svg"
      />
      <div
        class="text"
      >
        <p class="code">KS-HM-ZH</p>
        <p class="url">next.openbroadcast.ch</p>
      </div>
      <div class="step">2</div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.view {
  //background: rgb(var(--c-black) / 5%);
  //background: rgb(105 198 227);
  background: rgb(158 105 227);
  padding: 100px;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
}

.qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;

  .step {
    position: absolute;
    bottom: 44px;
    left: 50px;
    font-size: 2.5rem;
    border: 4px solid currentColor;
    width: 60px;
    height: 60px;
    border-radius: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &--store {
    color: rgb(var(--c-white));
    background: rgb(var(--c-black));
    .badge {
      margin-top: 3rem;
      height: 75px;

      > img {
        width: 200px;
      }
    }
  }
  &--voucher {
    color: rgb(var(--c-black));
    background: rgb(var(--c-white));
    .text {
      height: 75px;
      margin-top: 3rem;
      margin-bottom: 0rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      .code {
        padding-top: 0.5rem;
        font-size: 2.5rem;
      }

      .url {
        color: rgb(var(--c-black) / 50%);
      }

    }
  }
}

</style>
