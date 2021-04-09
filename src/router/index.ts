import { createRouter, createWebHistory } from 'vue-router';
import OnAir from '@/views/OnAir.vue';
import Discover from '@/views/Discover.vue';
import ArtistDetail from '@/views/catalog/ArtistDetail.vue';
import PlaylistDetail from '@/views/catalog/PlaylistDetail.vue';
import PlaylistList from '@/components/catalog/playlist/List.vue';
import ArtisttList from '@/components/catalog/artist/List.vue';
import MediatList from '@/components/catalog/media/List.vue';

const routes = [
  {
    path: '/',
    name: 'onAir',
    component: OnAir,
  },
  {
    path: '/discover/',
    name: 'discover',
    component: Discover,
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
        component: MediatList,
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
    component: Discover,
  },
  {
    path: '/collection/artists/:uid/',
    name: 'Artist Detail (Collection)',
    component: ArtistDetail,
  },
  {
    path: '/account/',
    name: 'Account',
    component: () => import(
      '@/views/Account.vue'
    ),
    children: [
      {
        path: 'settings/',
        component: () => import(
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
