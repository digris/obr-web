/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { getArtist, getPlaylist } from '@/api/catalog';

const state = {
  artists: [],
  playlists: [],
};

const getters = {
  // @ts-ignore
  artists: (state) => state.artists,
  // @ts-ignore
  artistByUid: (state) => (uid: string) => state.artists.find((obj) => obj.uid === uid),
  // @ts-ignore
  playlists: (state) => state.playlists,
  // @ts-ignore
  playlistByUid: (state) => (uid: string) => state.playlists.find((obj) => obj.uid === uid),
};

const mutations = {
  // @ts-ignore
  SET_ARTIST: (state, { artist }) => {
    // @ts-ignore
    const index = state.artists.findIndex((obj) => obj.uid === artist.uid);
    if (index > -1) {
      state.artists[index] = artist;
    } else {
      state.artists.push(artist);
    }
  },
  // @ts-ignore
  SET_PLAYLIST: (state, { playlist }) => {
    // @ts-ignore
    const index = state.playlists.findIndex((obj) => obj.uid === playlist.uid);
    if (index > -1) {
      state.playlists[index] = playlist;
    } else {
      state.playlists.push(playlist);
    }
  },
};

const actions = {
  // @ts-ignore
  loadArtist: async (context, uid: string) => {
    const artist = await getArtist(uid);
    context.commit('SET_ARTIST', { artist });
  },
  // @ts-ignore
  loadPlaylist: async (context, uid: string) => {
    const playlist = await getPlaylist(uid);
    context.commit('SET_PLAYLIST', { playlist });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
