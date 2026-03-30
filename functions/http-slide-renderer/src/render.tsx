import fs from 'node:fs/promises'

import { Resvg } from '@resvg/resvg-js'
import satori from 'satori'

import { ArtistSlide } from '@/templates/ArtistSlide.js'
import { MediaSlide } from '@/templates/MediaSlide.js'
import type { Context } from '@/types/context.js'

const BASE_URL = 'https://openbroadcast.ch/api/v1/'

let fontData: ArrayBuffer | null = null

const templateMap = {
  'catalog.media': MediaSlide,
  'catalog.artist': ArtistSlide,
} as const

async function getFont() {
  if (!fontData) {
    const buf = await fs.readFile(new URL('./fonts/IBMPlexSans-Regular.woff', import.meta.url))

    fontData = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength)
  }
  return fontData
}

async function fetchContext(ct: string, uid: string) {
  // api pattern: ct: catalog.media -> catalog/media etc
  // https://openbroadcast.ch/api/v1/catalog/media/A8FE72BD/

  const path = `${ct.replace('.', '/')}/${uid}/`
  const url = `${BASE_URL}${path}`

  console.debug('fetch_context', { url })

  const res = await fetch(url)

  if (!res.ok) {
    throw new Error(`Failed to fetch context: ${res.status} ${res.statusText}`)
  }

  return res.json()
}

export async function renderSvg(ct: string, uid: string, width: number, height: number) {
  const font = await getFont()

  const context = (await fetchContext(ct, uid)) as Context

  const Template = templateMap[context.ct as keyof typeof templateMap]

  if (!Template) {
    throw new Error(`No template for ct: ${context.ct}`)
  }

  console.debug(context)

  const svg = await satori(<Template {...context} />, {
    width,
    height,
    fonts: [
      {
        name: 'IBMPlexSans',
        data: font,
        weight: 400,
        style: 'normal',
      },
    ],
  })

  return svg
}

export async function renderPng(svg: string) {
  const resvg = new Resvg(svg, {
    logLevel: 'debug',
    font: {
      loadSystemFonts: false,
    },
    textRendering: 1,
  })
  return resvg.render().asPng()
}
