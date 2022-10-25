import { storeToRefs } from "pinia";
import { useNotificationStore } from "@/stores/notification";

export const useNotification = () => {
  const { messages } = storeToRefs(useNotificationStore());
  const { notify, setMessageSeen } = useNotificationStore();
  return {
    messages,
    notify,
    setMessageSeen,
  };
};
