import { DateTime } from "luxon";
import { defineStore } from "pinia";

import { getProgram } from "@/api/broadcast";
import type { Emission } from "@/typings/api";

export type AnnotatedEmission = Emission & {
  dtStart: DateTime;
  dtEnd: DateTime;
};

interface State {
  emissions: Array<AnnotatedEmission>;
}

const annotateEmissions = (emissions: Array<Emission>): Array<AnnotatedEmission> => {
  return emissions.map((emission: Emission) => {
    return {
      ...emission,
      // @ts-ignore
      dtStart: DateTime.fromISO(emission.timeStart),
      // @ts-ignore
      dtEnd: DateTime.fromISO(emission.timeEnd),
    };
  });
};

export const useProgramStore = defineStore("program", {
  state: (): State => ({
    emissions: [],
  }),
  // persist: true,
  actions: {
    async loadEmissions(date: DateTime): Promise<void> {
      const program = await getProgram(date.toISODate());
      this.emissions = annotateEmissions(program.emissions);
    },
  },
});
