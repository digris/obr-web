export type RenderRequest = {
  ct: string
  uid: string
  width: number
  height: number
  format: 'jpg' | 'png' | 'webp' | 'svg'
}

const PATH_REGEX =
  /^\/render\/(?<ct>[a-z.]+):(?<uid>[A-Z0-9]{8})\/(?<width>\d+)x(?<height>\d+)\.(?<format>jpg|png|webp|svg)$/i

export function parseRequest(path: string): RenderRequest {
  // normalize trailing slash
  path = path.replace(/\/+$/, '')

  const match = path.match(PATH_REGEX)

  if (!match?.groups) {
    throw new Error('Invalid path')
  }

  const { ct, uid, width, height, format } = match.groups

  return {
    ct,
    uid,
    width: Number(width),
    height: Number(height),
    format: format as RenderRequest['format'],
  }
}
