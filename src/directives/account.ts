const loginRequired = {
  created(el: any, binding: any, vnode: any, prevVnode: any) {
    console.debug('created', el, binding, vnode, prevVnode);
    console.debug('created binding', binding);
    el.addEventListener('click', (e:any) => {
      console.debug('click', e);
      e.preventDefault();
    });
  },
  beforeMount() {
    console.debug('beforeMount');
  },
  mounted() {
    console.debug('mounted');
  },
  beforeUpdate() {
    console.debug('beforeUpdate');
  },
  updated() {
    console.debug('updated');
  },
  beforeUnmount() {
    console.debug('beforeUnmount');
  },
  unmounted() {
    console.debug('unmounted');
  },
};

export { loginRequired };
