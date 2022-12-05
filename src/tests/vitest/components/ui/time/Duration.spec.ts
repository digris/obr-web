import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import Duration from "@/components/ui/time/Duration.vue";

describe("Duration", () => {
  it("render 0s", () => {
    const wrapper = mount(Duration, { props: { seconds: 0 } });
    expect(wrapper.text()).toEqual("0s");
  });
  it("render 30s", () => {
    const wrapper = mount(Duration, { props: { seconds: 30 } });
    expect(wrapper.text()).toEqual("30s");
  });
  it("render 5m", () => {
    const wrapper = mount(Duration, { props: { seconds: 300 } });
    expect(wrapper.text()).toEqual("05:00");
  });
  it("render 1h", () => {
    const wrapper = mount(Duration, { props: { seconds: 3600 } });
    expect(wrapper.text()).toEqual("01:00:00");
  });
  // rounding
  it("render 3699 (not rounded)", () => {
    const wrapper = mount(Duration, { props: { seconds: 3699 } });
    expect(wrapper.text()).toEqual("01:01:39");
  });
  it("render 3699 (rounded 5m)", () => {
    const wrapper = mount(Duration, { props: { seconds: 3699, roundSeconds: 5 * 60 } });
    expect(wrapper.text()).toEqual("01:00:00");
  });
  it("render 15 (rounded 30s)", () => {
    const wrapper = mount(Duration, { props: { seconds: 15, roundSeconds: 30 } });
    expect(wrapper.text()).toEqual("15s");
  });
  it("render 40 (rounded 30s)", () => {
    const wrapper = mount(Duration, { props: { seconds: 40, roundSeconds: 30 } });
    expect(wrapper.text()).toEqual("30s");
  });
  it("render 50 (rounded 30s)", () => {
    const wrapper = mount(Duration, { props: { seconds: 50, roundSeconds: 30 } });
    expect(wrapper.text()).toEqual("01:00");
  });
});
