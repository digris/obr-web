import { config } from '../config.js'

const IMAGE_BASE_URL = config.image.baseUrl
const CONTRAST_BREAKPOINT = config.image.contrastBreakpoint

export function getContrastColor(rgb: [number, number, number]): [number, number, number] {
  const mean = rgb.reduce((s, b) => s + b, 0) / 3
  return mean > CONTRAST_BREAKPOINT ? [0, 0, 0] : [255, 255, 255]
}

export function getImageUrl(path: string, width: number, height: number): string {
  return `${IMAGE_BASE_URL}crop/${width}x${height}/${path}`
}
