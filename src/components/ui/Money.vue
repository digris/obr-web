<script>
export default {
  name: "Money",
  props: {
    value: {
      type: Number,
      required: true,
    },
    includeCurrency: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      currency: {
        symbol: "CHF",
      },
      locale: "de-CH",
    };
  },
  computed: {
    symbol() {
      return this.currency.symbol;
    },
    valueDisplay() {
      return "?"; // TODO: remove once we know the prices..
      /*
      const options = {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      };
      let valueStr = this.value.toLocaleString(this.locale, options);
      if (valueStr.endsWith(".00")) {
        valueStr = valueStr.replace(".00", ".-");
      }
      return valueStr;
      */
    },
  },
};
</script>

<template>
  <span class="money">
    <span v-if="includeCurrency" class="symbol" v-text="`${symbol}&nbsp;`" />
    <span class="value" v-text="valueDisplay" />
  </span>
</template>

<style lang="scss" scoped>
.money {
  display: inline-flex;
  align-items: flex-end;
}
</style>
