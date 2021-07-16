import { APIClient } from '@/api/Client';
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

async function getArtists(limit: number, offset: number) {
  const url = ARTIST_ENDPOINT;
  const params = {
    limit, offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getArtist(uid: string) {
  const url = `${ARTIST_ENDPOINT}${uid}/`;
  const response = await APIClient.get(url);
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

// const check = () => 'checked.';

async function getWTFPlaylists(limit: number, offset: number) {
  const url = PLAYLIST_ENDPOINT;
  const params = {
    limit, offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getPlaylist(uid: string) {
  const url = `${PLAYLIST_ENDPOINT}${uid}/`;
  const params = {
    expand: 'media_set',
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export {
  getMoods,
  getArtists,
  getArtist,
  getMedia,
  getMediaTags,
  getWTFPlaylists,
  getPlaylist,
};
