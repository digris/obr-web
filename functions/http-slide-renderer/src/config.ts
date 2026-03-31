export const config = {
  api: {
    baseUrl: process.env.API_BASE_URL ?? 'https://openbroadcast.ch/api/v1/',
  },
  image: {
    baseUrl: process.env.IMAGE_BASE_URL ?? 'https://openbroadcast.ch/images/',
    jpeg: {
      defaultQuality: 90,
      minQuality: 5,
      step: 5,
      maxBytesCap: 100 * 1024,
    },
    resize: {
      fit: 'cover' as const,
    },
    contrastBreakpoint: 86,
  },
}
