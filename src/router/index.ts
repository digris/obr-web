import { createRouter, createWebHistory } from "vue-router";
import { isEqual } from "lodash-es";
import { DateTime } from "luxon";
// import store from "@/store";
import NotFound from "@/views/NotFound.vue";
// import OnAir from '@/views/OnAir.vue';
import Radio from "@/views/Radio.vue";
import Program from "@/views/Program.vue";
import Discover from "@/views/Discover.vue";
import Collection from "@/views/Collection.vue";
import Account from "@/views/Account.vue";
import Page from "@/views/cms/Page.vue";
import EditorList from "@/components/broadcast/editor/List.vue";
import MoodList from "@/components/catalog/mood/List.vue";
import MoodDetail from "@/views/catalog/MoodDetail.vue";
import ArtistList from "@/components/catalog/artist/List.vue";
import ArtistDetail from "@/views/catalog/ArtistDetail.vue";
import PlaylistList from "@/components/catalog/playlist/List.vue";
import PlaylistDetail from "@/views/catalog/PlaylistDetail.vue";
import EditorDetail from "@/views/broadcast/EditorDetail.vue";
import MediaList from "@/components/catalog/media/List.vue";
import MediaDetail from "@/views/catalog/MediaDetail.vue";
import AccountLogin from "@/components/account/Login.vue";
import AccountEmailLogin from "@/components/account/EmailLogin.vue";
import AccountSettings from "@/components/account/settings/Settings.vue";
import DiscoverHeader from "@/layouts/DiscoverHeader.vue";
import Searchbar from "@/components/filter/Searchbar.vue";
//
import ProtoBase from "@/views/proto/Proto.vue";
import ProtoIcons from "@/views/proto/Icons.vue";
import ProtoRating from "@/views/proto/Rating.vue";

import { getUser } from "@/api/account";
import { setBodyColorTheme } from "@/utils/color";
import { parseFilterQuery } from "@/utils/filter";

const isAuthenticated = async () => {
  const user = await getUser();
  return user;
};

const routes = [
  {
    path: "/",
    name: "home",
    component: Radio,
    meta: {
      colorTheme: "live",
    },
  },
  {
    path: "/program/",
    name: "programRedirect",
    redirect: () => {
      const now = DateTime.now();
      return {
        name: "program",
        params: {
          date: now.toISODate(),
        },
      };
    },
  },
  {
    path: "/program/:date(\\d{4}-\\d{2}-\\d{2})/",
    // path: "/program/:date(\\d{4}-\\d{2}-\\d{2})/:time(\\d{2}:\\d{2})?/",
    name: "program",
    components: {
      default: Program,
    },
    props: {
      default: (route: any) => ({
        date: DateTime.fromISO(route.params.date),
        // timeStr: route.params.time,
      }),
    },
  },
  {
    path: "/discover/",
    name: "discover",
    component: Discover,
    redirect: {
      name: "discoverMoods",
    },
    meta: {
      title: "Discover",
    },
    children: [
      {
        path: "moods/",
        name: "discoverMoods",
        // component: MoodList,
        components: {
          default: MoodList,
          header: DiscoverHeader,
        },
        meta: {
          title: "Moods",
        },
      },
      {
        path: "playlists/",
        name: "discoverPlaylists",
        components: {
          default: PlaylistList,
          header: DiscoverHeader,
        },
        props: {
          default: (route: any) => ({
            // query: route.query,
            query: parseFilterQuery(route.query),
          }),
          header: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: "artists/",
        name: "discoverArtists",
        components: {
          default: ArtistList,
          header: DiscoverHeader,
        },
        props: {
          default: (route: any) => ({
            // query: route.query,
            query: parseFilterQuery(route.query),
          }),
          header: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: "tracks/",
        name: "discoverMedia",
        components: {
          default: MediaList,
          header: DiscoverHeader,
        },
        props: {
          default: (route: any) => ({
            query: parseFilterQuery(route.query),
            showListActions: true,
          }),
          header: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: "editors/",
        name: "discoverEditors",
        components: {
          default: EditorList,
          header: DiscoverHeader,
        },
      },
      // testing nested detail components
      {
        path: "/discover/moods/:uid/",
        name: "moodDetail",
        components: {
          default: MoodDetail,
        },
        props: {
          default: (route: any) => ({
            uid: route.params.uid,
            query: parseFilterQuery(route.query),
          }),
        },
        meta: {
          colorTheme: "dark",
        },
      },
      {
        path: "/discover/playlists/:uid/",
        name: "playlistDetail",
        components: {
          default: PlaylistDetail,
        },
        props: {
          default: (route: any) => ({
            uid: route.params.uid,
          }),
        },
        meta: {
          colorTheme: "dark",
        },
      },
      {
        path: "/discover/artists/:uid/",
        name: "artistDetail",
        components: {
          default: ArtistDetail,
        },
        props: {
          default: (route: any) => ({
            uid: route.params.uid,
          }),
        },
        meta: {
          colorTheme: "dark",
        },
      },
      {
        path: "/discover/tracks/:uid/",
        name: "mediaDetail",
        components: {
          default: MediaDetail,
        },
        props: {
          default: (route: any) => ({
            uid: route.params.uid,
          }),
        },
        meta: {
          colorTheme: "dark",
        },
      },
      {
        path: "/discover/editors/:uid/",
        name: "editorDetail",
        components: {
          default: EditorDetail,
        },
        props: {
          default: (route: any) => ({
            uid: route.params.uid,
            query: parseFilterQuery(route.query),
          }),
        },
        meta: {
          colorTheme: "dark",
        },
      },
    ],
  },
  // {
  //   path: '/discover/playlists/:uid/',
  //   name: 'playlistDetail',
  //   component: PlaylistDetail,
  //   props: (route: any) => ({
  //     uid: route.params.uid,
  //   }),
  //   meta: {
  //     colorTheme: 'dark',
  //   },
  // },
  // {
  //   path: '/discover/moods/:uid/',
  //   name: 'moodDetail',
  //   component: MoodDetail,
  //   props: (route: any) => ({
  //     uid: route.params.uid,
  //     query: parseFilterQuery(route.query),
  //   }),
  //   meta: {
  //     colorTheme: 'dark',
  //   },
  // },
  // {
  //   path: '/discover/artists/:uid/',
  //   name: 'artistDetail',
  //   component: ArtistDetail,
  //   props: (route: any) => ({
  //     uid: route.params.uid,
  //   }),
  //   meta: {
  //     colorTheme: 'dark',
  //   },
  // },
  // {
  //   path: "/discover/tracks/:uid/",
  //   name: "mediaDetail",
  //   component: MediaDetail,
  //   props: (route: any) => ({
  //     uid: route.params.uid,
  //   }),
  //   meta: {
  //     colorTheme: "dark",
  //   },
  // },
  // {
  //   path: '/discover/editors/:uid/',
  //   name: 'editorDetail',
  //   component: EditorDetail,
  //   props: (route: any) => ({
  //     uid: route.params.uid,
  //   }),
  //   meta: {
  //     colorTheme: 'dark',
  //   },
  // },
  {
    path: "/collection/",
    name: "collection",
    component: Collection,
    /*
    beforeEnter: async (to: any, from: any, next: any) => {
      const authenticated = await isAuthenticated();
      if (!authenticated) {
        next({ name: 'accountLogin' });
      } else {
        next();
      }
    },
    */
    redirect: {
      name: "collectionMedia",
    },
    children: [
      {
        path: "tracks/",
        name: "collectionMedia",
        components: {
          default: MediaList,
          searchbar: Searchbar,
        },
        props: {
          default: (route: any) => ({
            scope: "collection",
            query: route.query,
            showListActions: true,
          }),
          searchbar: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: "shows/",
        name: "collectionPlaylists",
        components: {
          default: PlaylistList,
          searchbar: Searchbar,
        },
        props: {
          default: (route: any) => ({
            scope: "collection",
            query: route.query,
          }),
          searchbar: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: "artists/",
        name: "collectionArtists",
        components: {
          default: ArtistList,
          searchbar: Searchbar,
        },
        props: {
          default: (route: any) => ({
            scope: "collection",
            query: route.query,
          }),
          searchbar: (route: any) => ({
            filter: route.query,
          }),
        },
      },
    ],
  },
  {
    path: "/account/",
    name: "Account",
    component: Account,
    redirect: {
      name: "accountSettings",
    },
    children: [
      {
        path: "login/",
        name: "accountLogin",
        component: AccountLogin,
        beforeEnter: async (to: any, from: any, next: any) => {
          const authenticated = await isAuthenticated();
          if (authenticated) {
            next({ name: "accountSettings" });
          } else {
            next();
          }
        },
      },
      {
        path: "settings/",
        name: "accountSettings",
        component: AccountSettings,
        beforeEnter: async (to: any, from: any, next: any) => {
          const authenticated = await isAuthenticated();
          if (!authenticated) {
            next({ name: "accountLogin" });
          } else {
            next();
          }
        },
      },
      {
        path: "email-login/:signedEmail?/",
        name: "accountEmailLogin",
        component: AccountEmailLogin,
      },
    ],
  },
  {
    path: "/proto/",
    name: "proto",
    component: ProtoBase,
    redirect: {
      name: "protoIcons",
    },
    children: [
      {
        path: "icons/",
        name: "protoIcons",
        component: ProtoIcons,
      },
      {
        path: "rating/",
        name: "protoRating",
        component: ProtoRating,
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    name: "page",
    component: Page,
    props: (route: any) => ({
      path: route.path,
    }),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  // @ts-ignore
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (from && to.name === from.name && isEqual(to.params, from.params)) {
      return false;
    }
    return savedPosition || { left: 0, top: 0 };
  },
});

router.beforeEach((to, from, next) => {
  const theme = to.meta?.colorTheme ?? "light";
  // @ts-ignore
  setBodyColorTheme(theme);
  next();
});

router.beforeEach(async (to, from, next) => {
  const node = to.matched
    .slice()
    .reverse()
    .find((r) => r.meta && r.meta.title);
  if (node) {
    // await store.dispatch("ui/setTitle", node?.meta?.title);
  }
  next();
});

// router.beforeEach((to, from, next) => {
//   // eslint-disable-next-line no-param-reassign
//   to.meta.activated = true;
//   // eslint-disable-next-line no-param-reassign
//   from.meta.activated = false;
//   next();
// });

// router.afterEach((to, from) => {
//   const toDepth = to.path.split('/').length;
//   const fromDepth = from.path.split('/').length;
//   // eslint-disable-next-line no-param-reassign
//   to.meta.transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left';
// });

export default router;
