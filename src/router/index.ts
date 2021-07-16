import { createRouter, createWebHistory } from 'vue-router';
import NotFound from '@/views/NotFound.vue';
import OnAir from '@/views/OnAir.vue';
import Discover from '@/views/Discover.vue';
import Collection from '@/views/Collection.vue';
import Account from '@/views/Account.vue';
import ArtistDetail from '@/views/catalog/ArtistDetail.vue';
import PlaylistDetail from '@/views/catalog/PlaylistDetail.vue';
import PlaylistList from '@/components/catalog/playlist/List.vue';
import ArtisttList from '@/components/catalog/artist/List.vue';
import MoodList from '@/components/catalog/mood/List.vue';
import MediaList from '@/components/catalog/media/List.vue';
import AccountLogin from '@/components/account/Login.vue';
import AccountEmailLogin from '@/components/account/EmailLogin.vue';
import AccountSettings from '@/components/account/settings/Settings.vue';
import Filterbar from '@/components/filter/Filterbar.vue';

import { getCurrentUser } from '@/api/account';

const isAuthenticated = async () => {
  const user = await getCurrentUser();
  return user;
};

const routes = [
  {
    path: '/',
    name: 'home',
    component: OnAir,
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
        props: {
          primaryColor: [255, 255, 255],
        },
      },
      {
        path: 'playlists/',
        name: 'discoverPlaylists',
        // component: PlaylistList,
        components: {
          default: PlaylistList,
          filterbar: Filterbar,
        },
        props: {
          default: {
            primaryColor: [255, 255, 255],
          },
          primaryColor: [255, 255, 255],
        },
      },
      {
        path: 'artists/',
        name: 'discoverArtists',
        // component: ArtisttList,
        // props: {
        //   primaryColor: [255, 255, 255],
        // },
        components: {
          default: ArtisttList,
          filterbar: Filterbar,
        },
        props: {
          default: {
            primaryColor: [255, 255, 255],
          },
          primaryColor: [255, 255, 255],
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
          default: {
            primaryColor: [255, 255, 255],
          },
          primaryColor: [255, 255, 255],
        },
      },
    ],
  },
  {
    path: '/discover/playlists/:uid/',
    name: 'playlistDetail',
    component: PlaylistDetail,
  },
  {
    path: '/discover/artists/:uid/',
    name: 'artistDetail',
    component: ArtistDetail,
    props: {
      primaryColor: [102, 102, 102],
    },
  },
  {
    path: '/collection/',
    name: 'collection',
    component: Collection,
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
          default: {
            scope: 'collection',
            primaryColor: [255, 255, 255],
          },
          primaryColor: [255, 255, 255],
        },
        // component: MediaList,
        // props: {
        //   scope: 'collection',
        // },
      },
      {
        path: 'shows/',
        name: 'collectionAPlaylists',
        component: PlaylistList,
      },
    ],
  },
  {
    path: '/collection/artists/:uid/',
    name: 'Artist Detail (Collection)',
    component: ArtistDetail,
  },
  {
    path: '/account/',
    name: 'Account',
    component: Account,
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
  // @ts-ignore
  // scrollBehavior(to, from, savedPosition) {
  //   if (savedPosition) {
  //     return savedPosition;
  //   }
  //   return { x: 0, y: 0 };
  // },
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { x: 0, y: 0 };
  },
});

// router.afterEach((to, from) => {
//   const toDepth = to.path.split('/').length;
//   const fromDepth = from.path.split('/').length;
//   // eslint-disable-next-line no-param-reassign
//   to.meta.transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left';
// });

export default router;
