import type { Editor } from "@/typings/api";
import { defineStore } from "pinia";
import { getEditor } from "@/api/broadcast";

interface State {
  editors: Array<Editor>;
}

export const useBroadcastStore = defineStore("broadcast", {
  state: (): State => ({
    editors: [],
  }),
  getters: {
    editorByUid: (state: State) => {
      return (uid: string) => state.editors.find((editor) => editor.uid === uid);
    },
  },
  actions: {
    async loadEditor(uid: string): Promise<void> {
      const editor = await getEditor(uid);
      console.debug("stores/broadcast: loadEditor", editor);
      const index = this.editors.findIndex((obj) => obj.uid === uid);
      if (index > -1) {
        this.editors[index] = editor;
      } else {
        this.editors.push(editor);
      }
    },
  },
});
