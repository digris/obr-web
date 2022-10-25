import type { Artist, Media, Mood } from "@/typings/api";
import { defineStore } from "pinia";
import { without } from "lodash-es";
import { getArtist, getMediaDetail, getMood, getPlaylist } from "@/api/catalog";

interface State {
  artists: Array<Artist>;
  media: Array<Media>;
  moods: Array<Mood>;
  playlists: Array<any>;
  //
  loading: Array<string>;
}

export const useCatalogStore = defineStore("catalog", {
  state: (): State => ({
    artists: [],
    media: [],
    moods: [],
    playlists: [],
    //
    loading: [],
  }),
  getters: {
    artistByUid: (state: State) => (uid: string) => {
      return state.artists.find((obj) => obj.uid === uid) || null;
    },
    mediaByUid: (state: State) => (uid: string) => {
      return state.media.find((obj) => obj.uid === uid) || null;
    },
    moodByUid: (state: State) => (uid: string) => {
      return state.moods.find((obj) => obj.uid === uid) || null;
    },
    playlistByUid: (state: State) => (uid: string) => {
      return state.playlists.find((obj) => obj.uid === uid) || null;
    },
  },
  actions: {
    async loadArtist(uid: string): Promise<void> {
      if (this.artistByUid(uid)) {
        console.debug(`already loaded: ${uid}`);
        return;
      }
      const objKey = `artist-${uid}`;
      if (this.loading.includes(objKey)) {
        console.debug(`already loading: ${objKey}`);
        return;
      }
      this.loading.push(objKey);
      this.artists.push(await getArtist(uid));
      this.loading = without(this.loading, objKey);
    },
    async loadMedia(uid: string): Promise<void> {
      if (!this.mediaByUid(uid)) {
        this.media.push(await getMediaDetail(uid));
      }
    },
    async loadMood(uid: string): Promise<void> {
      if (!this.moodByUid(uid)) {
        this.moods.push(await getMood(uid));
      }
    },
    async loadPlaylist(uid: string): Promise<void> {
      if (!this.playlistByUid(uid)) {
        this.playlists.push(await getPlaylist(uid));
      }
    },
  },
});
