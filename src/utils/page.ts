import store from "@/store";

const setPageTitle = async (title: string) => {
  await store.dispatch("ui/setTitle", title);
};

export { setPageTitle };
