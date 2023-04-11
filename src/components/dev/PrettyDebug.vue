<script lang="ts">
import { computed, defineComponent } from "vue";

const formatJSON = (value: any) => {
  let json = JSON.stringify(value, null, 4);
  json = json.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return json.replace(
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g,
    (match) => {
      let cls = "number";
      if (/^"/.test(match)) {
        if (/:$/.test(match)) {
          cls = "key";
        } else {
          cls = "string";
        }
      } else if (/true|false/.test(match)) {
        cls = "boolean";
      } else if (/null/.test(match)) {
        cls = "null";
      }
      return `<span class="${cls}">${match}</span>`;
    }
  );
};

export default defineComponent({
  props: {
    title: {
      type: String,
      default: null,
      required: false,
    },
    value: {
      type: Object,
      default: () => {},
    },
    visible: {
      type: Boolean,
      default: true,
    },
  },
  setup(props) {
    const formatted = computed(() => {
      const html = formatJSON(props.value);
      if (props.title) {
        return `<span class="comment"># ${props.title}</span><br>${html}`;
      }
      return html;
    });
    return {
      formatted,
    };
  },
});
</script>

<template>
  <div v-if="visible" class="debug-panel">
    <pre v-html="formatted" />
  </div>
</template>

<style lang="scss" scoped>
.debug-panel {
  padding: 1rem;
  font-weight: 300;
  font-size: 0.8rem;
  background: #222;

  :deep(pre) {
    color: white;

    .comment {
      color: #a09f9f;
    }

    .string {
      color: #6def6d;
    }

    .number {
      color: darkorange;
    }

    .boolean {
      color: #f8ff1a;
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
