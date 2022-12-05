import { APIClient } from "@/api/client";
// import settings from "@/settings";
import { useAPIBaseUrl } from "@/composables/api";

const { APIBaseUrl } = useAPIBaseUrl();

const MOOD_ENDPOINT = `${APIBaseUrl.value}catalog/moods/`;
const PLAYLIST_ENDPOINT = `${APIBaseUrl.value}catalog/playlists/`;
const ARTIST_ENDPOINT = `${APIBaseUrl.value}catalog/artists/`;
const MEDIA_ENDPOINT = `${APIBaseUrl.value}catalog/media/`;

async function getMoods(limit: number, offset: number) {
  const url = MOOD_ENDPOINT;
  const params = {
    limit,
    offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getMood(uid: string) {
  const url = `${MOOD_ENDPOINT}${uid}/`;
  const response = await APIClient.get(url);
  return response.data;
}

async function getArtists(
  limit: number,
  offset: number,
  filter: any,
  ordering: Array<string> = []
) {
  const url = ARTIST_ENDPOINT;
  const params = {
    limit,
    offset,
    ordering: ordering.join(","),
    ...filter,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getArtistsTags(filter: any) {
  const url = `${ARTIST_ENDPOINT}tags/`;
  const params = {
    ...filter,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getArtist(uid: string) {
  const url = `${ARTIST_ENDPOINT}${uid}/`;
  const params = {
    expand: ["tags", "identifiers"],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getMedia(limit: number, offset: number, filter: any, ordering: Array<string> = []) {
  const url = MEDIA_ENDPOINT;
  const params = {
    limit,
    offset,
    ordering: ordering.join(","),
    ...filter,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getMediaTags(filter: any) {
  const url = `${MEDIA_ENDPOINT}tags/`;
  const params = {
    ...filter,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getMediaDetail(uid: string) {
  const url = `${MEDIA_ENDPOINT}${uid}/`;
  const params = {
    expand: ["tags", "identifiers"],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

// const check = () => 'checked.';

async function getPlaylists(
  limit: number,
  offset: number,
  filter: any,
  ordering: Array<string> = [],
  expand: Array<string> = []
) {
  const url = PLAYLIST_ENDPOINT;
  const params = {
    limit,
    offset,
    ordering: ordering.join(","),
    expand,
    ...filter,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getPlaylistsTags(filter: any) {
  const url = `${PLAYLIST_ENDPOINT}tags/`;
  const params = {
    ...filter,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getPlaylist(uid: string) {
  const url = `${PLAYLIST_ENDPOINT}${uid}/`;
  const params = {
    expand: ["media_set", "tags", "editor", "duration", "latest_emission"],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export {
  getArtist,
  getArtists,
  getArtistsTags,
  getMedia,
  getMediaDetail,
  getMediaTags,
  getMood,
  getMoods,
  getPlaylist,
  getPlaylists,
  getPlaylistsTags,
};
