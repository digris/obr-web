<script lang="ts">
import { defineComponent, computed } from 'vue';

const formatJSON = (value: object) => {
  let json = JSON.stringify(value, null, 4);
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, (match) => {
    let cls = 'number';
    if (/^"/.test(match)) {
      if (/:$/.test(match)) {
        cls = 'key';
      } else {
        cls = 'string';
      }
    } else if (/true|false/.test(match)) {
      cls = 'boolean';
    } else if (/null/.test(match)) {
      cls = 'null';
    }
    return `<span class="${cls}">${match}</span>`;
  });
};

export default defineComponent({
  props: {
    value: {
      type: Object,
      default: () => {
      },
    },
    visible: {
      type: Boolean,
      default: true,
    },
  },
  setup(props) {
    const formatted = computed(() => {
      return formatJSON(props.value);
    });
    return {
      formatted,
    };
  },
});
</script>

<template>
  <div
    v-if="visible"
    class="debug-panel"
  >
    <pre
      v-html="formatted"
    />
  </div>
</template>

<style lang="scss" scoped>
.debug-panel {
  font-size: 0.8rem;
  font-weight: 300;
  background: #222;
  padding: 1rem;

  :deep(pre) {
    color: white;
    .string {
      color: #6def6d;
    }

    .number {
      color: darkorange;
    }

    .boolean {
      color: blue;
    }

    .null {
      color: #d26fd2;
    }

    .key {
      color: #00e6ff;
    }
  }
}
</style>
