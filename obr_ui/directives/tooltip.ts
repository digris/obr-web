const TooltipDirective = {
  beforeMount(el: any, binding: any) {
    // eslint-disable-next-line no-param-reassign
    el.style.setProperty("--tooltip-text", `"${binding.value}"`);
    // eslint-disable-next-line no-param-reassign
    el.classList.add("has-tooltip");
  },
};

export { TooltipDirective };
