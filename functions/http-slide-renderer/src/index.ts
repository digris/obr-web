import type { Request, Response } from '@google-cloud/functions-framework'
import { http } from '@google-cloud/functions-framework'

import { logger } from './logger.js'
import type { RenderRequest } from './parser.js'
import { parseLogoRequest, parseSlideRequest } from './parser.js'
import { encodeJpeg, encodePng, renderLogo, renderSlide, svgToPng } from './render.js'

type FormatOptions = {
  maxBytes?: number
}

function parseFormatOptions(req: Request): FormatOptions {
  const raw = req.query.maxBytes

  if (!raw) return {}

  const value = Number(raw)
  if (!Number.isFinite(value) || value <= 0) {
    throw new Error('Invalid maxBytes')
  }

  return {
    maxBytes: Math.min(value, 100 * 1024),
  }
}

async function respond(
  svg: string,
  req: RenderRequest,
  res: Response,
  options: FormatOptions = {},
) {
  switch (req.format) {
    case 'svg': {
      res.set('Content-Type', 'image/svg+xml')
      return res.status(200).send(svg)
    }

    case 'png': {
      const png = await svgToPng(svg)

      const img = await encodePng(png, req.width, req.height)

      res.set('Content-Type', 'image/png')
      return res.status(200).send(img)
    }

    case 'jpg': {
      const png = await svgToPng(svg)
      const img = await encodeJpeg(png, req.width, req.height, options.maxBytes)

      res.set('Content-Type', 'image/jpeg')
      return res.status(200).send(img)
    }
  }
}
async function render(req: Request, res: Response) {
  const splat = req.params.splat ?? []
  const [kind, ...rest] = splat

  logger.info(
    {
      path: req.path,
      params: req.params,
      splat,
      kind,
      rest,
    },
    'request_received',
  )

  const formatOptions = parseFormatOptions(req)

  try {
    let parsed: RenderRequest
    let svg: string

    switch (kind) {
      case 'logo': {
        parsed = parseLogoRequest(rest.join('/'))
        logger.info({ parsed }, 'parsed_logo_request')
        svg = await renderLogo(parsed.rgb)
        break
      }
      case 'slide': {
        parsed = parseSlideRequest(rest.join('/'))
        logger.info({ parsed }, 'parsed_slide_request')
        svg = await renderSlide(parsed.ct, parsed.uid, parsed.kind)
        break
      }
      default:
        throw new Error(`Unknown kind: ${kind}`)
    }

    return await respond(svg, parsed, res, formatOptions)
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error'

    logger.warn({ path: req.path, params: req.params, error: message }, 'render_error')

    res.status(400).send({ error: message })
  }
}

http('render', render)
