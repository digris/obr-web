export type LogoRenderRequest = {
  type: 'logo'
  rgb?: [number, number, number]
  width: number
  height: number
  format: 'jpg' | 'png' | 'svg'
}

export type SlideRenderRequest = {
  type: 'slide'
  ct: string
  uid: string
  width: number
  height: number
  kind: 'cover' | 'full'
  format: 'jpg' | 'png' | 'svg'
}

export type RenderRequest = LogoRenderRequest | SlideRenderRequest

const LOGO_PATH_REGEX =
  /^(?:(?<rgb>\d{1,3}:\d{1,3}:\d{1,3})\/)?(?<width>\d+)x(?<height>\d+)\.(?<format>jpg|png|svg)$/i

export function parseLogoRequest(path: string): LogoRenderRequest {
  path = path.replace(/\/+$/, '')

  const match = path.match(LOGO_PATH_REGEX)

  if (!match?.groups) {
    throw new Error('Invalid path')
  }

  const { rgb, width, height, format } = match.groups

  let parsedRgb: [number, number, number] | undefined

  if (rgb) {
    const parts = rgb.split(':').map(Number)

    if (parts.length !== 3 || parts.some((n) => n < 0 || n > 255)) {
      throw new Error('Invalid RGB value')
    }

    parsedRgb = parts as [number, number, number]
  }

  return {
    type: 'logo',
    rgb: parsedRgb,
    width: Number(width),
    height: Number(height),
    format: format as LogoRenderRequest['format'],
  }
}

const SLIDE_PATH_REGEX =
  /^(?<kind>cover|full)\/(?<ct>[a-z.]+):(?<uid>[A-Z0-9]{8})\/(?<width>\d+)x(?<height>\d+)\.(?<format>jpg|png|svg)$/i

export function parseSlideRequest(path: string): SlideRenderRequest {
  console.log('parse_slide_request', { path })

  path = path.replace(/\/+$/, '')

  console.log('path', { path })

  const match = path.match(SLIDE_PATH_REGEX)

  if (!match?.groups) {
    throw new Error('Invalid path')
  }

  const { ct, uid, width, height, kind, format } = match.groups

  return {
    type: 'slide',
    ct,
    uid,
    width: Number(width),
    height: Number(height),
    kind: kind as SlideRenderRequest['kind'],
    format: format as SlideRenderRequest['format'],
  }
}
