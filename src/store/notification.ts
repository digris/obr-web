/* eslint no-shadow: ["error", { "allow": ["state"] }] */

export interface Message {
  key: string,
  body: string,
  seen: boolean,
  ttl: number | null,
}

export interface State {
  messages: Array<object>,
}

const state: State = {
  messages: [],
};

const getters = {
  messages: (state: any) => state.messages,
};

const mutations = {
  ADD_MESSAGE: (state: any, message: Message) => {
    state.messages.push(message);
  },
  DELETE_MESSAGE: (state: any, key: string) => {
    const index = state.messages.findIndex((m: Message) => m.key === key);
    if (index > -1) {
      state.messages.splice(index, 1);
    }
  },
};

const actions = {
  addMessage: async (context: any, message: Message) => {
    const key = Math.random().toString(36).substring(2);
    const { ttl } = message;
    context.commit('ADD_MESSAGE', { ...message, key, seen: null });
    if (ttl) {
      setTimeout(() => {
        context.commit('DELETE_MESSAGE', key);
      }, ttl * 1000);
    }
  },
  setMessageSeen: async (context: any, message: Message) => {
    context.commit('DELETE_MESSAGE', message.key);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
