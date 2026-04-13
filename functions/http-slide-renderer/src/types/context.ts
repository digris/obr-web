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
  image?: {
    url: string
    path: string
    rgb?: [number, number, number]
  }
}

export type PlaylistContext = {
  ct: 'catalog.playlist'
  uid: string
  name: string
  image?: {
    url: string
    path: string
    rgb?: [number, number, number]
  }
  editor?: {
    ct: string
    uid: string
    name: string
    image?: {
      url: string 
      path: string
      rgb?: [number, number, number]
    }
  }
}

export type EmissionContext = {
  ct: 'broadcast.emission'
  uid: string
  timeStart: string
  timeEnd: string
  playlist: {
    ct: string
    uid: string
    name: string
    seriesDisplay: string
    editorDisplay: string
    image?: {
      url: string
      path: string
      rgb?: [number, number, number]
    }
  }
}

export type Context = MediaContext | ArtistContext | PlaylistContext | EmissionContext
