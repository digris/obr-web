/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { getEditor } from "@/api/broadcast";

const state = {
  editors: [],
};

const getters = {
  // @ts-ignore
  editors: (state) => state.editors,
  // @ts-ignore
  editorByUid: (state) => (uid: string) => state.editors.find((obj) => obj.uid === uid),
};

const mutations = {
  // @ts-ignore
  SET_PLAYLIST: (state, { editor }) => {
    // @ts-ignore
    const index = state.editors.findIndex((obj) => obj.uid === editor.uid);
    if (index > -1) {
      state.editors[index] = editor;
    } else {
      state.editors.push(editor);
    }
  },
};

const actions = {
  // @ts-ignore
  loadEditor: async (context, uid: string) => {
    const editor = await getEditor(uid);
    context.commit("SET_PLAYLIST", { editor });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
