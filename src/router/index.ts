import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';
import NotFound from '@/views/NotFound.vue';
import OnAir from '@/views/OnAir.vue';
import Program from '@/views/Program.vue';
import Discover from '@/views/Discover.vue';
import Collection from '@/views/Collection.vue';
import Account from '@/views/Account.vue';
import Page from '@/views/cms/Page.vue';
import PType from '@/views/PType.vue';
import EditorList from '@/components/broadcast/editor/List.vue';
import MoodList from '@/components/catalog/mood/List.vue';
import MoodDetail from '@/views/catalog/MoodDetail.vue';
import ArtistList from '@/components/catalog/artist/List.vue';
import ArtistDetail from '@/views/catalog/ArtistDetail.vue';
import PlaylistList from '@/components/catalog/playlist/List.vue';
import PlaylistDetail from '@/views/catalog/PlaylistDetail.vue';
import EditorDetail from '@/views/broadcast/EditorDetail.vue';
import MediaList from '@/components/catalog/media/List.vue';
import MediaDetail from '@/views/catalog/MediaDetail.vue';
import AccountLogin from '@/components/account/Login.vue';
import AccountEmailLogin from '@/components/account/EmailLogin.vue';
import AccountSettings from '@/components/account/settings/Settings.vue';
// eslint-disable-next-line import/no-unresolved
import SearchbarAlt from '@/components/filter/SearchbarAlt.vue';

import { getUser } from '@/api/account';
import { setBodyColorTheme } from '@/utils/color';
import { parseFilterQuery } from '@/utils/filter';

const isAuthenticated = async () => {
  const user = await getUser();
  return user;
};

const routes = [
  {
    path: '/',
    name: 'home',
    component: OnAir,
    meta: {
      colorTheme: 'live',
    },
  },
  {
    path: '/program/',
    name: 'program',
    component: Program,
  },
  {
    path: '/discover/',
    name: 'discover',
    component: Discover,
    redirect: {
      name: 'discoverMoods',
    },
    meta: {
      title: 'Discover',
    },
    children: [
      {
        path: 'moods/',
        name: 'discoverMoods',
        component: MoodList,
        meta: {
          title: 'Moods',
        },
      },
      {
        path: 'playlists/',
        name: 'discoverPlaylists',
        components: {
          default: PlaylistList,
          searchbar: SearchbarAlt,
        },
        props: {
          default: (route: any) => ({
            query: route.query,
          }),
          searchbar: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: 'artists/',
        name: 'discoverArtists',
        components: {
          default: ArtistList,
          searchbar: SearchbarAlt,
        },
        props: {
          default: (route: any) => ({
            query: route.query,
          }),
          searchbar: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: 'tracks/',
        name: 'discoverMedia',
        components: {
          default: MediaList,
          searchbar: SearchbarAlt,
        },
        props: {
          default: (route: any) => ({
            query: route.query,
          }),
          searchbar: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: 'editors/',
        name: 'discoverEditors',
        component: EditorList,
      },
    ],
  },
  {
    path: '/discover/playlists/:uid/',
    name: 'playlistDetail',
    component: PlaylistDetail,
    props: (route: any) => ({
      uid: route.params.uid,
    }),
    meta: {
      colorTheme: 'dark',
    },
  },
  {
    path: '/discover/moods/:uid/',
    name: 'moodDetail',
    component: MoodDetail,
    props: (route: any) => ({
      uid: route.params.uid,
      query: parseFilterQuery(route.query),
    }),
    meta: {
      colorTheme: 'dark',
    },
  },
  {
    path: '/discover/artists/:uid/',
    name: 'artistDetail',
    component: ArtistDetail,
    props: (route: any) => ({
      uid: route.params.uid,
    }),
    meta: {
      colorTheme: 'dark',
    },
  },
  {
    path: '/discover/tracks/:uid/',
    name: 'mediaDetail',
    component: MediaDetail,
    props: (route: any) => ({
      uid: route.params.uid,
    }),
    meta: {
      colorTheme: 'dark',
    },
  },
  {
    path: '/discover/editors/:uid/',
    name: 'editorDetail',
    component: EditorDetail,
    props: (route: any) => ({
      uid: route.params.uid,
    }),
    meta: {
      colorTheme: 'dark',
    },
  },
  {
    path: '/collection/',
    name: 'collection',
    component: Collection,
    /*
    beforeEnter: async (to: object, from: object, next: any) => {
      const authenticated = await isAuthenticated();
      if (!authenticated) {
        next({ name: 'accountLogin' });
      } else {
        next();
      }
    },
    */
    redirect: {
      name: 'collectionMedia',
    },
    children: [
      {
        path: 'tracks/',
        name: 'collectionMedia',
        components: {
          default: MediaList,
          searchbar: SearchbarAlt,
        },
        props: {
          default: (route: any) => ({
            scope: 'collection',
            query: route.query,
          }),
          searchbar: (route: any) => ({
            filter: route.query,
          }),
        },
      },
      {
        path: 'shows/',
        name: 'collectionAPlaylists',
        // component: PlaylistList,
        components: {
          default: PlaylistList,
          searchbar: SearchbarAlt,
        },
        props: {
          default: (route: any) => ({
            scope: 'collection',
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
    path: '/account/',
    name: 'Account',
    component: Account,
    redirect: {
      name: 'accountSettings',
    },
    children: [
      {
        path: 'login/',
        name: 'accountLogin',
        component: AccountLogin,
        beforeEnter: async (to: object, from: object, next: any) => {
          const authenticated = await isAuthenticated();
          if (authenticated) {
            next({ name: 'accountSettings' });
          } else {
            next();
          }
        },
      },
      {
        path: 'settings/',
        name: 'accountSettings',
        component: AccountSettings,
        beforeEnter: async (to: object, from: object, next: any) => {
          const authenticated = await isAuthenticated();
          if (!authenticated) {
            next({ name: 'accountLogin' });
          } else {
            next();
          }
        },
      },
      {
        path: 'email-login/:signedEmail?/',
        name: 'accountEmailLogin',
        component: AccountEmailLogin,
      },
    ],
  },
  {
    path: '/ptype/',
    name: 'ptype',
    component: PType,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'page',
    component: Page,
    props: (route: any) => ({
      path: route.path,
    }),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory('/'),
  // @ts-ignore
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 };
  },
});

router.beforeEach((to, from, next) => {
  const theme = to.meta?.colorTheme ?? 'light';
  // @ts-ignore
  setBodyColorTheme(theme);
  next();
});

router.beforeEach(async (to, from, next) => {
  const node = to.matched.slice().reverse().find((r) => r.meta && r.meta.title);
  if (node) {
    await store.dispatch('ui/setTitle', node?.meta?.title);
  }
  // await store.dispatch('ui/setTitle', node?.meta?.title ?? 'open broadcast radio');
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
