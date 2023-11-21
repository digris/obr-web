<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useClipboard, useShare } from "@vueuse/core";

import QRCodeVoucher from "@/components/account/qrcode/QRCodeVoucher.vue";
import Datetime from "@/components/ui/date/Datetime.vue";
import type { UserVoucher } from "@/typings/api";

export default defineComponent({
  components: {
    Datetime,
    QRCodeVoucher,
  },
  props: {
    voucher: {
      type: Object as PropType<UserVoucher>,
      required: true,
    },
  },
  setup(props) {
    const { t } = useI18n();
    const link = computed(() => {
      const path = `/#${props.voucher.codeDisplay}`;
      const href = `${window.location.origin}${path}`;
      const display = `${window.location.hostname}${path}`;
      return {
        href,
        display,
      };
    });
    const { share, isSupported: shareSupported } = useShare();
    const { copy: copyCode, copied: copiedCode } = useClipboard({
      source: props.voucher.codeDisplay,
    });
    const shareCode = () => {
      share({
        title: `Code: ${props.voucher.codeDisplay}`,
        url: link.value.href,
      });
    };
    return {
      t,
      shareCode,
      shareSupported,
      copyCode,
      copiedCode,
      link,
    };
  },
});
</script>
<template>
  <div class="voucher" :class="{ 'is-invalid': !voucher.isValid }">
    <QRCodeVoucher class="qr-code" :voucher="voucher" />
    <div class="details">
      <div @click.prevent="copyCode" class="code-display">
        {{ voucher.codeDisplay }}
        <transition name="copied">
          <div v-if="copiedCode" class="copied">
            <div class="copied__text">Copied to clipboard</div>
          </div>
        </transition>
      </div>
      <div class="num-days" @click="copyCode">
        <i18n-t keypath="subscription.validNumDays" :plural="voucher.numDays" />
      </div>
      <div class="usage">
        <div class="usage__count">
          <i18n-t keypath="subscription.numUsedAndTotal">
            <span v-text="voucher.numUsed" />
            <span v-text="voucher.maxNumUse" />
          </i18n-t>
        </div>
        <div class="usage__date">
          <i18n-t keypath="subscription.validUntilDate">
            <Datetime :value="voucher.validUntil" :display-time="false" />
          </i18n-t>
        </div>
      </div>
      <div v-if="shareSupported" class="share">
        <span @click.prevent="shareCode" class="button" v-text="`Share Code`" />
      </div>
    </div>
    <div class="invalid-notice" v-if="!voucher.isValid">
      <span>EXPIRED / USED</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";
@use "@/style/elements/button";

.voucher {
  display: grid;
  grid-gap: 2rem;
  grid-template-columns: 169px 1fr;
  padding: 1rem;
  background: rgb(var(--c-dark) / 5%);
  color: rgb(var(--c-dark));
  position: relative;

  &.is-invalid {
    color: rgb(var(--c-dark) / 25%);
    pointer-events: none;

    .qr-code {
      opacity: 0.25;
    }

    .invalid-notice {
      top: 0;
      position: absolute;
      height: 100%;
      left: 1rem;
      display: flex;
      align-items: center;
      justify-content: center;

      > span {
        color: rgb(var(--c-light));
        background: rgb(var(--c-red));

        @include typo.bold;

        padding: 1rem;
        display: inline-flex;
        width: 200px;
        justify-content: center;
      }

      @include responsive.bp-medium {
        height: calc(200px + 2rem);
        width: 100%;
        left: 0;
      }
    }
  }

  .details {
    display: flex;
    flex-direction: column;
    align-items: center;

    .code-display {
      @include typo.x-large;
      @include typo.bold;

      line-height: var(--t-fs-x-large);
      cursor: pointer;
      position: relative;
      user-select: text;

      .copied {
        @include typo.small;

        top: -30px;
        position: absolute;
        width: 100%;
        color: rgb(var(--c-light));
        line-height: var(--t-fs-small);
        display: flex;
        justify-content: center;

        &__text {
          background: rgb(var(--c-dark));
          padding: 0.5rem;
        }
      }
    }

    .num-days {
      @include typo.large;

      line-height: 1.5;
    }

    .usage {
      align-items: center;
      line-height: 1.5;
      white-space: break-spaces;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      justify-content: flex-end;

      &__count {
        display: flex;
        justify-content: center;
        text-align: center;
        text-transform: capitalize;
      }

      &__date {
        display: flex;
        text-align: center;
        justify-content: center;
      }
    }

    .share {
      padding: 0.5rem 1rem 0;

      > span {
        @include typo.large;

        text-decoration: underline;
        cursor: pointer;
      }
    }
  }

  @include responsive.bp-medium {
    grid-template-columns: unset;
    grid-template-rows: 169px 1fr;
    background: transparent;

    .qr-code {
      margin-top: 0;
      justify-self: center;
    }

    .code-display {
      margin: 1rem 0;
    }
  }
}

.copied-enter-active,
.copied-leave-active {
  transition: opacity 200ms, transform 200ms;
}

.copied-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.copied-leave-to {
  opacity: 0;
}
</style>
