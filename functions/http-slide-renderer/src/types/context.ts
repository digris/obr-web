export type MediaContext = {
  ct: 'catalog.media'
  uid: string
  name: string
  artistDisplay: string
  releaseDisplay: string
  releases: {
    name: string
    image?: {
      url: string
      path: string
      rgb?: [number, number, number]
    }
  }[]
}

export type ArtistContext = {
  ct: 'catalog.artist'
  uid: string
  name: string
}

export type Context = MediaContext | ArtistContext
