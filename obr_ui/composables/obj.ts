import { computed, isReactive, isRef, ref, unref, watchEffect } from "vue";

const useObjKey = (obj: any) => {
  const objKey = ref("");
  const setObjKey = () => {
    const o = unref(obj);
    // console.debug("useObjKey: setObjKey", {
    //   obj,
    //   o,
    // });
    objKey.value = o?.ct && o?.uid ? `${o.ct}:${o.uid}` : "";
  };
  if (isRef(obj)) {
    // console.debug("useObjKey: isRef", obj);
    watchEffect(setObjKey);
  } else if (isReactive(obj)) {
    // console.debug("useObjKey: isReactive", obj);
    watchEffect(setObjKey);
  } else {
    // console.debug("useObjKey: non-ref value", obj);
    setObjKey();
  }
  return {
    objKey,
  };
};

const useObjCtUid = (objKey: string) => {
  const parts = computed(() => {
    if (!objKey) {
      return [];
    }
    return objKey.split(":");
  });
  const objCt = computed(() => {
    return parts.value.length === 2 ? parts.value[0] : null;
  });
  const objUid = computed(() => {
    return parts.value.length === 2 ? parts.value[1] : null;
  });
  return {
    objCt,
    objUid,
  };
};

export { useObjCtUid, useObjKey };
