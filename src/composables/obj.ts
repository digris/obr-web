import { computed } from "vue";

const useObjKey = (obj: object) => {
  const objKey = computed(() => {
    return obj?.ct && obj?.uid ? `${obj.ct}:${obj.uid}` : "";
  });
  return {
    objKey,
  };
};

export { useObjKey };
