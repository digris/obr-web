/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { getArtist } from '@/api/catalog';

const state = {
  artists: [],
};

const getters = {
  artists: (state) => state.artists,
  artistByUid: (state) => (uid) => state.artists.find((obj) => obj.uid === uid),
};

const mutations = {
  // SET_ARTISTS: (state, { payload }) => {
  //   payload.forEach((artist) => {
  //     const index = state.artists.findIndex((obj) => obj.uid === artist.uid);
  //     if (index > -1) {
  //       state.artists[index] = artist;
  //     } else {
  //       state.artists.push(artist);
  //     }
  //   });
  // },
  SET_ARTIST: (state, { artist }) => {
    const index = state.artists.findIndex((obj) => obj.uid === artist.uid);
    if (index > -1) {
      state.artists[index] = artist;
    } else {
      state.artists.push(artist);
    }
  },
};

const actions = {
  // loadArtists: async (context) => {
  //   const url = ARTIST_ENDPOINT;
  //   const params = {
  //     limit: 20,
  //   };
  //   APIClient.get(url, { params }).then((response) => {
  //     context.commit('SET_ARTISTS', { payload: response.data.results });
  //   }).catch((e) => {
  //     console.warn('unable to load artists', e);
  //   });
  // },
  loadArtist: async (context, uid) => {
    const artist = await getArtist({ uid });
    context.commit('SET_ARTIST', { artist });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
