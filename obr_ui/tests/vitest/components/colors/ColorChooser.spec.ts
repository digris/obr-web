import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import ColorChoser from "@/components/colors/ColorChooser.vue";

describe("ColorChoser", () => {
  it("renders properly", () => {
    const wrapper = mount(ColorChoser, { props: { msg: "Hello Vitest" } });
    expect(wrapper.text()).toContain("");
  });
});
