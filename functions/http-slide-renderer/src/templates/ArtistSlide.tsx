import type { ArtistContext } from '@/types/context.js'

import { getContrastColor, getImageUrl } from './utils.js'

export function ArtistSlide({ name, image }: ArtistContext) {
  const size = 440

  const imageUrl = image ? getImageUrl(image.path, size, size) : undefined
  // const imageUrl = undefined

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
              width: size,
              height: size,
              objectFit: 'cover',
              borderRadius: 2,
              boxShadow: `2px 2px 8px 6px rgba(0, 0, 0, 0.1)`,
            }}
          />
        ) : (
          <div
            style={{
              width: size,
              height: size,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 16,
            }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 602 602"
              stroke={`rgb(${fgColor.join(' ')})`}
              strokeWidth={28}
              fill="none"
              width={size - 64}
              height={size - 64}
            >
              <polygon points="539 301 138 486.99 138 115.01 539 301" />
              <rect x="138.01" y="107" width="119.01" height="387.98" />
              <rect x="345.01" y="106.99" width="119.01" height="387.98" />
              <circle cx="301" cy="301" r="287" />
            </svg>
          </div>
        )}
      </div>
    </div>
  )
}
