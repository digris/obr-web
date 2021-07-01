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
import MediaList from '@/components/catalog/media/List.vue';
import AccountLogin from '@/components/account/Login.vue';
import AccountEmailLogin from '@/components/account/EmailLogin.vue';
import AccountSettings from '@/components/account/settings/Settings.vue';

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
      name: 'discoverPlaylists',
    },
    children: [
      {
        path: 'playlists/',
        name: 'discoverPlaylists',
        component: PlaylistList,
      },
      {
        path: 'artists/',
        name: 'discoverArtists',
        component: ArtisttList,
      },
      // {
      //   path: 'artists/:uid/',
      //   component: () => import(
      //     /* webpackChunkName: "catalog-artist-detail" */
      //     '@/components/catalog/artist/Detail.vue'
      //   ),
      // },
      {
        path: 'tracks/',
        name: 'discoverMedia',
        component: MediaList,
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
        path: 'artists/',
        name: 'collectionArtists',
        component: ArtisttList,
      },
      {
        path: 'tracks/',
        name: 'collectionMedia',
        component: MediaList,
        props: {
          scope: 'collection',
        },
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
