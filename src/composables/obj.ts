import { computed } from "vue";

const useObjKey = (obj: object) => {
  console.debug("obj", obj);
  const objKey = computed(() => {
    return obj?.ct && obj?.uid ? `${obj.ct}:${obj.uid}` : "";
  });
  return {
    objKey,
  };
};

const useObjCtUid = (objKey: string) => {
  const parts = computed(() => {
    return objKey.split(":");
  });
  const objCt = computed(() => {
    return parts.value[0];
  });
  const objUid = computed(() => {
    return parts.value[1];
  });
  return {
    objCt,
    objUid,
  };
};

export { useObjKey, useObjCtUid };
