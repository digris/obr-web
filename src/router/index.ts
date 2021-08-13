import { createRouter, createWebHistory } from 'vue-router';
import NotFound from '@/views/NotFound.vue';
import OnAir from '@/views/OnAir.vue';
import Discover from '@/views/Discover.vue';
import Collection from '@/views/Collection.vue';
import Account from '@/views/Account.vue';
import EditorList from '@/components/broadcast/editor/List.vue';
import MoodList from '@/components/catalog/mood/List.vue';
import ArtistList from '@/components/catalog/artist/List.vue';
import ArtistDetail from '@/views/catalog/ArtistDetail.vue';
import PlaylistList from '@/components/catalog/playlist/List.vue';
import PlaylistDetail from '@/views/catalog/PlaylistDetail.vue';
import MediaList from '@/components/catalog/media/List.vue';
import MediaDetail from '@/views/catalog/MediaDetail.vue';
import AccountLogin from '@/components/account/Login.vue';
import AccountEmailLogin from '@/components/account/EmailLogin.vue';
import AccountSettings from '@/components/account/settings/Settings.vue';
import Filterbar from '@/components/filter/Filterbar.vue';

import { getUser } from '@/api/account';
import { setBodyColorTheme } from '@/utils/color';

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
    path: '/discover/',
    name: 'discover',
    component: Discover,
    redirect: {
      name: 'discoverMoods',
    },
    children: [
      {
        path: 'moods/',
        name: 'discoverMoods',
        component: MoodList,
      },
      {
        path: 'playlists/',
        name: 'discoverPlaylists',
        // component: PlaylistList,
        components: {
          default: PlaylistList,
          filterbar: Filterbar,
        },
      },
      {
        path: 'artists/',
        name: 'discoverArtists',
        components: {
          default: ArtistList,
          filterbar: Filterbar,
        },
      },
      {
        path: 'tracks/',
        name: 'discoverMedia',
        components: {
          default: MediaList,
          filterbar: Filterbar,
        },
        props: {
          default: (route: any) => ({
            query: route.query,
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
          filterbar: Filterbar,
        },
        props: {
          default: (route: any) => ({
            scope: 'collection',
            query: route.query,
          }),
        },
      },
      {
        path: 'shows/',
        name: 'collectionAPlaylists',
        // component: PlaylistList,
        components: {
          default: PlaylistList,
          filterbar: Filterbar,
        },
        props: {
          default: (route: any) => ({
            scope: 'collection',
            query: route.query,
          }),
        },
      },
    ],
  },
  {
    path: '/collection/artists/:uid/',
    name: 'Artist Detail (Collection)',
    component: ArtistDetail,
    props: (route: any) => ({
      uid: route.params.uid,
    }),
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
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory('/'),
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
