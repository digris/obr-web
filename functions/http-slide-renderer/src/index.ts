import { parse } from 'node:path'

import type { Request, Response } from '@google-cloud/functions-framework'
import { http } from '@google-cloud/functions-framework'
import sharp from 'sharp'

import { parseRequest } from './parser.js'
import { renderPng, renderSvg } from './render.js'

async function render(req: Request, res: Response) {
  try {
    const parsed = parseRequest(req.path)

    console.log('render_request', parsed)

    const svg = await renderSvg(parsed.ct, parsed.uid, parsed.width, parsed.height)

    console.log('svg', svg.length)

    // res.set("Content-Type", "application/json")
    // res.status(200).send(parsed)

    switch (parsed.format) {
      case 'svg':
        res.set('Content-Type', 'image/svg+xml')
        res.status(200).send(svg)
        break
      case 'png': {
        const png = await renderPng(svg)
        console.log('png', png.length)
        res.set('Content-Type', `image/png`)
        res.status(200).send(png)
        break
      }
      case 'jpg': {
        const png = await renderPng(svg)
        const jpg = await sharp(png).jpeg({ quality: 50 }).toBuffer()
        console.log('jpg', jpg.length)
        res.set('Content-Type', `image/jpeg`)
        res.status(200).send(jpg)
        break
      }
      case 'webp': {
        const png = await renderPng(svg)
        const webp = await sharp(png).webp({ quality: 50 }).toBuffer()
        console.log('webp', webp.length)
        res.set('Content-Type', `image/webp`)
        res.status(200).send(webp)
        break
      }
      default:
        throw new Error(`Unsupported format: ${parsed.format}`)
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error'

    console.warn('render_error', {
      path: req.path,
      error: message,
    })

    res.status(400).send({ error: message })
  }
}

// 👇 THIS is the key line for dev mode
http('render', render)
