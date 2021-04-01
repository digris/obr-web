import { APIClient } from '@/api/Client';
import settings from '@/settings';

const ARTIST_ENDPOINT = `${settings.API_BASE_URL}catalog/artists/`;

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

async function getMedia() {
  return [];
}

export { getArtists, getArtist, getMedia };
