import { mount } from "@vue/test-utils";
import { DateTime } from "luxon";
import { describe, expect, it } from "vitest";

import Datetime from "@/components/ui/date/Datetime.vue";

describe("Datetime", () => {
  it("full date (string): ", () => {
    const wrapper = mount(Datetime, {
      props: {
        value: "2025-01-01T12:00:00+01:00",
      },
    });
    expect(wrapper.text()).toBe("1.1.202512:00");
  });
  it("full date (DateTime obj): ", () => {
    const wrapper = mount(Datetime, {
      props: {
        value: DateTime.fromISO("2025-01-01T12:00:00+01:00"),
      },
    });
    expect(wrapper.text()).toBe("1.1.202512:00");
  });
  it("date only: ", () => {
    const wrapper = mount(Datetime, {
      props: {
        value: "2025-01-01T12:00:00+01:00",
        displayTime: false,
      },
    });
    expect(wrapper.text()).toBe("1.1.2025");
  });
  it("time only: ", () => {
    const wrapper = mount(Datetime, {
      props: {
        value: "2025-01-01T12:00:00+01:00",
        displayDate: false,
      },
    });
    expect(wrapper.text()).toBe("12:00");
  });
});
