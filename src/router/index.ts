import { createRouter, createWebHistory } from 'vue-router';
import OnAir from '../views/OnAir.vue';

const routes = [
  {
    path: '/',
    name: 'onAir',
    component: OnAir,
  },
  {
    path: '/discover/',
    name: 'discover',
    component: () => import(
      /* webpackChunkName: "discover" */
      '@/views/Discover.vue'
    ),
    children: [
      {
        path: 'artists/',
        name: 'discoverArtists',
        component: () => import(
          /* webpackChunkName: "catalog-artists-list" */
          '@/components/catalog/artist/List.vue'
        ),
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
        component: () => import(
          /* webpackChunkName: "catalog-media-list" */
          '@/components/catalog/media/List.vue'
        ),
      },
    ],
  },
  {
    path: '/discover/artists/:uid/',
    name: 'artistDetail',
    component: () => import(
      /* webpackChunkName: "catalog-artist-detail" */
      '@/views/catalog/ArtistDetail.vue'
    ),
  },
  {
    path: '/collection/',
    name: 'collection',
    component: () => import(
      /* webpackChunkName: "collection" */
      '@/views/Discover.vue'
    ),
  },
  {
    path: '/collection/artists/:uid/',
    name: 'Artist Detail (Collection)',
    component: () => import(
      /* webpackChunkName: "catalog-artist-detail" */
      '@/views/catalog/ArtistDetail.vue'
    ),
  },
  {
    path: '/account/',
    name: 'Account',
    component: () => import(
      /* webpackChunkName: "account" */
      '@/views/Account.vue'
    ),
    children: [
      {
        path: 'settings/',
        component: () => import(
          /* webpackChunkName: "account-settings" */
          '@/components/account/Settings.vue'
        ),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory('/'),
  routes,
});

// router.afterEach((to, from) => {
//   const toDepth = to.path.split('/').length;
//   const fromDepth = from.path.split('/').length;
//   // eslint-disable-next-line no-param-reassign
//   to.meta.transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left';
// });

export default router;
