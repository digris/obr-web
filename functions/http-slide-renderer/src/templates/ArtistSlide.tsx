import type { ArtistContext } from '@/types/context.js'

export function ArtistSlide({ name }: ArtistContext) {
  return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        height: '100%',
        backgroundColor: '#111',
        color: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 32,
        fontFamily: 'IBMPlexSans, sans-serif',
      }}
    >
      {name}
    </div>
  )
}
