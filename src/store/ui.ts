/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

export interface Viewport {
  top: number;
  left: number;
  height: number;
  width: number;
}

export interface State {
  // primaryColor: Array<number>,
  title: string;
  primaryColor: [number, number, number];
  viewport: Viewport;
}

const state: State = {
  title: "open broadcast radio",
  primaryColor: [0, 0, 0],
  viewport: {
    top: 0,
    left: 0,
    height: 0,
    width: 0,
  },
};

const getters = {
  viewport: (state: State) => state.viewport,
  // isMobile: (state: State) => state.viewport.width < 500,
  title: (state: State) => state.title,
  primaryColor: (state: State) => state.primaryColor,
};

const mutations = {
  SET_VIEWPORT: (state: State, viewport: Viewport) => {
    state.viewport = viewport;
  },
  SET_TITLE: (state: State, title: string) => {
    state.title = title;
  },
  SET_PRIMARY_COLOR: (state: State, color: [number, number, number]) => {
    state.primaryColor = color;
  },
};

const actions = {
  setViewport: async (context: any, viewport: Viewport) => {
    context.commit("SET_VIEWPORT", viewport);
  },
  setTitle: async (context: any, title: string) => {
    context.commit("SET_TITLE", title);
  },
  setPrimaryColor: async (context: any, color: [number, number, number]) => {
    context.commit("SET_PRIMARY_COLOR", color);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
