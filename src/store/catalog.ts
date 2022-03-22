/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { getMediaDetail, getMood, getArtist, getPlaylist } from "@/api/catalog";

const state = {
  media: [],
  moods: [],
  artists: [],
  playlists: [],
  //
  loading: {},
};

const getters = {
  // @ts-ignore
  media: (state) => state.media,
  // @ts-ignore
  mediaByUid: (state) => (uid: string) => state.media.find((obj) => obj.uid === uid),
  // @ts-ignore
  moods: (state) => state.moods,
  // @ts-ignore
  moodByUid: (state) => (uid: string) => state.moods.find((obj) => obj.uid === uid),
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
  SET_MEDIA: (state, { media }) => {
    // @ts-ignore
    const index = state.media.findIndex((obj) => obj.uid === media.uid);
    if (index > -1) {
      state.media[index] = media;
    } else {
      state.media.push(media);
    }
  },
  // @ts-ignore
  SET_MOOD: (state, { mood }) => {
    // @ts-ignore
    const index = state.moods.findIndex((obj) => obj.uid === mood.uid);
    if (index > -1) {
      state.moods[index] = mood;
    } else {
      state.moods.push(mood);
    }
  },
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
  // @ts-ignore
  SET_LOADING: (state, { objKey, promise }) => {
    state.loading[objKey] = promise;
  },
};

const actions = {
  // @ts-ignore
  loadMedia: async (context, uid: string) => {
    const media = await getMediaDetail(uid);
    context.commit("SET_MEDIA", { media });
  },
  // @ts-ignore
  loadMood: async (context, uid: string) => {
    const mood = await getMood(uid);
    context.commit("SET_MOOD", { mood });
  },
  // @ts-ignore
  loadArtist: async (context, uid: string) => {
    if (context.getters.artistByUid(uid)) {
      return null;
    }
    const objKey = `artist-${uid}`;
    if (context.state.loading[objKey]) {
      return context.state.loading[objKey];
    }
    const promise = getArtist(uid).then((artist) => {
      context.commit("SET_ARTIST", { artist });
    });
    context.commit("SET_LOADING", { objKey, promise });
    return promise;
  },
  // @ts-ignore
  loadPlaylist: async (context, uid: string) => {
    const playlist = await getPlaylist(uid);
    context.commit("SET_PLAYLIST", { playlist });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
