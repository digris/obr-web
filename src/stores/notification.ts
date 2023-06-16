import { defineStore } from "pinia";

export interface Action {
  label: string;
  url: string;
}

export interface Message {
  level: "info" | "success" | "error";
  body: string;
  key?: string;
  seen?: boolean;
  ttl?: number;
  action?: Action;
}

interface State {
  messages: Array<Message>;
}

export const useNotificationStore = defineStore("notification", {
  state: (): State => ({
    messages: [],
  }),
  actions: {
    setMessageSeen(key: string) {
      this.messages = this.messages.filter((m: Message) => m.key !== key);
    },
    async notify(message: Message): Promise<void> {
      const key = Math.random().toString(36).substring(2);
      const { ttl } = message;
      this.messages.push({
        ...message,
        key,
      });
      if (ttl) {
        setTimeout(
          () => {
            this.setMessageSeen(key);
          },
          ttl * 1000,
          this
        );
      }
    },
  },
});
