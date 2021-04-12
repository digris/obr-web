import { APIClient } from '@/api/Client';
import settings from '@/settings';

const PLAYLIST_ENDPOINT = `${settings.API_BASE_URL}catalog/playlists/`;
const ARTIST_ENDPOINT = `${settings.API_BASE_URL}catalog/artists/`;
const MEDIA_ENDPOINT = `${settings.API_BASE_URL}catalog/media/`;

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

async function getMedia(limit: number, offset: number, filter: Object) {
  const url = MEDIA_ENDPOINT;
  const filterStr = '';
  // const params = {
  //   limit, offset,
  // };
  const params = {
    limit, offset, ...filter,
  };
  // filter.forEach((f) => {
  //   const k = Object.keys(f)[0];
  //   const v = Object.values(f)[0];
  //   console.debug('filter - k, v', k, v);
  // });
  // console.debug('prms', { ...params, ...filter });
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
  getArtists, getArtist, getMedia, getWTFPlaylists, getPlaylist,
};
