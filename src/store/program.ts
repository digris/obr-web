/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
import { DateTime } from "luxon";
import { getProgram } from "@/api/broadcast";

export interface Emission {
  timeStart: DateTime;
  timeEnd: DateTime;
}

export interface State {
  emissions: Array<Emission>;
}

const state: State = {
  emissions: [],
};

const getters = {
  emissions: (state: State) => state.emissions,
};

const mutations = {
  SET_EMISSIONS: (state: State, emissions: Array<any>) => {
    const parsedEmissions: Array<Emission> = [];
    emissions.forEach((el) => {
      const emission = { ...el };
      emission.timeStart = DateTime.fromISO(emission.timeStart);
      emission.timeEnd = DateTime.fromISO(emission.timeEnd);
      parsedEmissions.push(emission);
    });
    state.emissions = parsedEmissions;
  },
};

const actions = {
  loadEmissions: async (context: any, date: string) => {
    const program = await getProgram(date);
    context.commit("SET_EMISSIONS", program.emissions);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
