import { APIClient } from '@/api/Client';
import settings from '@/settings';

const ARTIST_ENDPOINT = `${settings.API_BASE_URL}catalog/artists/`;
const MEDIA_ENDPOINT = `${settings.API_BASE_URL}catalog/media/`;

async function getArtists({ limit, offset }) {
  const url = ARTIST_ENDPOINT;
  const params = {
    limit, offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getArtist({ uid }) {
  const url = `${ARTIST_ENDPOINT}${uid}/`;
  const response = await APIClient.get(url);
  return response.data;
}

async function getMedia({ limit, offset }) {
  const url = MEDIA_ENDPOINT;
  const params = {
    limit, offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
  // const response = {
  //   data: {
  //     results: [
  //       { name: 'the name 1' },
  //       { name: 'the name 2' },
  //     ],
  //   },
  // };
  // return response.data;
}

export { getArtists, getArtist, getMedia };
