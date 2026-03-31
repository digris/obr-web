import type { MediaContext } from '@/types/context.js'

import { getContrastColor, getImageUrl } from './utils.js'

export function MediaSlide({ name, artistDisplay, releases }: MediaContext) {
  const image = releases.find((r) => r.image)?.image
  const size = 400

  const imageUrl = image ? getImageUrl(image.path, size, size) : undefined

  const bgColor = image?.rgb ?? [0, 0, 0]
  const fgColor = getContrastColor(bgColor)

  return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        height: '100%',
        backgroundColor: `rgb(${bgColor.join(' ')})`,
        color: `rgb(${fgColor.join(' ')})`,
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'IBMPlexSans, sans-serif',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 16,
        }}
      >
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={name}
            style={{
              width: 320,
              height: 320,
              objectFit: 'cover',
              borderRadius: 2,
              boxShadow: `2px 2px 8px 6px rgba(0, 0, 0, 0.1)`,
            }}
          />
        ) : (
          <div
            style={{
              width: 320,
              height: 320,
              backgroundColor: '#333',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: 2,
            }}
          >
            No Image
          </div>
        )}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            gap: 2,
          }}
        >
          <p
            style={{
              fontSize: 28,
              fontWeight: 600,
              margin: 0,
              maxWidth: 560,
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}
          >
            {name}
          </p>

          <p
            style={{
              fontSize: 28,
              margin: 0,
              maxWidth: 560,
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}
          >
            {artistDisplay}
          </p>
        </div>
      </div>
    </div>
  )
}
