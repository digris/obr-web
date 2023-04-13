<script lang="ts">
import { defineComponent } from "vue";

import "./vendor/cookieconsent.js";

import "./vendor/cookieconsent.scss";

const cc = window.initCookieConsent();

const OPTIONS = {
  current_lang: "en",
  autoclear_cookies: true,
  cookie_name: "_cc",
  cookie_expiration: 365,
  page_scripts: true,

  // auto_language: null, // default: null; could also be 'browser' or 'document'
  autorun: false,
  delay: 1000,
  // force_consent: false,
  // hide_from_bots: false,
  // remove_cookie_tables: false,
  // cookie_domain: location.hostname,
  // cookie_path: "/",
  // cookie_same_site: "Lax",
  // use_rfc_cookie: false,
  revision: 0,

  gui_options: {
    consent_modal: {
      layout: "box",
      position: "top left",
      transition: "slide",
    },
    settings_modal: {
      layout: "box",
      transition: "slide",
    },
  },
  languages: {
    en: {
      consent_modal: {
        title: "Cookies",
        description:
          "This website uses essential cookies to ensure its proper operation and tracking cookies to understand how you interact with it." +
          '<br>The latter will be set only after your consent. <button type="button" data-cc="c-settings" class="cc-link">Cookie settings</button>',
        primary_btn: {
          text: "Accept all",
          role: "accept_all", // 'accept_selected' or 'accept_all'
        },
        secondary_btn: {
          text: "Reject all",
          role: "accept_necessary", // 'settings' or 'accept_necessary'
        },
      },
      settings_modal: {
        title: "Title",
        save_settings_btn: "Save settings",
        accept_all_btn: "Accept all",
        reject_all_btn: "Reject all",
        close_btn_label: "Close",
        cookie_table_headers: [
          { col1: "Name" },
          { col2: "Domain" },
          { col3: "Expiration" },
          { col4: "Description" },
        ],
        blocks: [
          {
            title: "Cookie usage",
            description:
              'We use cookies to ensure the basic functionalities of the website and to enhance your online experience. You can choose for each category to opt-in/out whenever you want. For more details relative to cookies and other sensitive data, please read the full <a href="/legal/dpp/" class="cc-link">privacy policy</a>.',
          },
          {
            title: "Strictly necessary",
            description:
              "These cookies are essential for the proper functioning of my website. Without these cookies, the website would not work properly",
            toggle: {
              value: "necessary",
              enabled: true,
              readonly: true, // cookie categories with readonly=true are all treated as "necessary cookies"
            },
          },
          {
            title: "Analytics",
            description:
              "These cookies allow the website to remember the choices you have made in the past",
            toggle: {
              value: "analytics", // there are no default categories => you specify them
              enabled: false,
              readonly: false,
            },
            cookie_table: [
              {
                col1: "_ga^",
                col2: window.location.hostname,
                col3: "1 year",
                col4: "description ...",
                is_regex: true,
              },
            ],
          },
          // {
          //   title: "More information",
          //   description:
          //     'For any queries in relation to our policy on cookies and your choices, please <a class="cc-link" href="https://orestbida.com/contact">contact me</a>.',
          // },
        ],
      },
    },
  },
};

export default defineComponent({
  components: {},
  setup() {
    const onFirstAction = () => {
      console.debug("onFirstAction");
    };
    const onAccept = (cookie: any) => {
      console.debug("onAccept", cookie);
    };
    const onChange = (cookie: any, changed_preferences: any) => {
      console.debug("onChange", cookie, changed_preferences);
    };
    const options = {
      ...OPTIONS,
      onFirstAction,
      onAccept,
      onChange,
    };
    if (!document.getElementById("cc--main")) {
      // @ts-ignore
      cc.run(options);
    }
    return {};
  },
});
</script>

<template>
  <div />
</template>
