import { APIClient } from '@/api/client';
import settings from '@/settings';

const MOOD_ENDPOINT = `${settings.API_BASE_URL}catalog/moods/`;
const PLAYLIST_ENDPOINT = `${settings.API_BASE_URL}catalog/playlists/`;
const ARTIST_ENDPOINT = `${settings.API_BASE_URL}catalog/artists/`;
const MEDIA_ENDPOINT = `${settings.API_BASE_URL}catalog/media/`;

async function getMoods(limit: number, offset: number) {
  const url = MOOD_ENDPOINT;
  const params = {
    limit, offset,
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
) {
  const url = ARTIST_ENDPOINT;
  const params = {
    limit, offset, ...filter,
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
    expand: [
      'tags',
      'identifiers', // TODO: implement in serializer
    ],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getMedia(limit: number, offset: number, filter: any) {
  const url = MEDIA_ENDPOINT;
  const params = {
    limit, offset, ...filter,
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
    expand: [
      'tags',
    ],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

// const check = () => 'checked.';

async function getPlaylists(
  limit: number,
  offset: number,
  filter: any,
  expand: Array<string> = [],
) {
  const url = PLAYLIST_ENDPOINT;
  const params = {
    limit, offset, expand, ...filter,
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
    expand: [
      'media_set',
      'tags',
      'editor',
      'duration',
      'latest_emission',
    ],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export {
  getMoods,
  getMood,
  getArtists,
  getArtistsTags,
  getArtist,
  getMedia,
  getMediaTags,
  getMediaDetail,
  getPlaylists,
  getPlaylistsTags,
  getPlaylist,
};
