import { jsx as _jsx } from "react/jsx-runtime";
import fs from 'node:fs/promises';
import { Resvg } from '@resvg/resvg-js';
import satori from 'satori';
import sharp from 'sharp';
import { config } from './config.js';
import { ArtistSlide } from './templates/ArtistSlide.js';
import { LogoSlide } from './templates/LogoSlide.js';
import { MediaSlide } from './templates/MediaSlide.js';
import { PlaylistSlide } from './templates/PlaylistSlide.js';
import { EmissionSlide } from './templates/EmissionSlide.js';
const API_BASE_URL = config.api.baseUrl;
const IMAGE_RESIZE_FIT = config.image.resize.fit;
let fontData = null;
async function getFont() {
    if (!fontData) {
        const buf = await fs.readFile(new URL('./fonts/IBMPlexSans-Regular.woff', import.meta.url));
        fontData = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
    }
    return fontData;
}
async function fetchContext(ct, uid) {
    const parts = ct.split('.');
    const irregularPlural = {
        media: 'media',
    };
    if (parts.length !== 2) {
        throw new Error(`Invalid context type: ${ct}`);
    }
    const [app, model] = parts;
    if (!['catalog', 'broadcast'].includes(app)) {
        throw new Error(`Unsupported context app: ${app}`);
    }
    const modelPlural = irregularPlural[model] ?? `${model}s`;
    const path = `${app}/${modelPlural}/${uid}/`;
    const url = new URL(`${API_BASE_URL}${path}`);
    if (ct === 'catalog.playlist') {
        url.searchParams.set('expand', 'editor');
    }
    console.log('fetch_context', { ct, uid, url: url.href });
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`Failed to fetch context: ${res.status} ${res.statusText}`);
    }
    return (await res.json());
}
export async function renderLogo(rgb = [0, 0, 0]) {
    const svgOpts = {
        width: 640,
        height: 480,
        fonts: [],
    };
    return await satori(_jsx(LogoSlide, { rgb: rgb }), svgOpts);
}
export async function renderSlide(ct, uid, _kind) {
    const font = await getFont();
    const svgOpts = {
        width: 640,
        height: 480,
        fonts: [
            {
                name: 'IBMPlexSans',
                data: font,
                weight: 400,
                style: 'normal',
            },
        ],
    };
    const context = await fetchContext(ct, uid);
    console.log('context_response', { ct, uid, context });
    if (context.ct === 'catalog.media') {
        return await satori(_jsx(MediaSlide, { ...context }), svgOpts);
    }
    if (context.ct === 'catalog.artist') {
        return await satori(_jsx(ArtistSlide, { ...context }), svgOpts);
    }
    if (context.ct === 'catalog.playlist') {
        return await satori(_jsx(PlaylistSlide, { ...context }), svgOpts);
    }
    if (context.ct === 'broadcast.emission') {
        return await satori(_jsx(EmissionSlide, { ...context }), svgOpts);
    }
    throw new Error(`Unsupported context type: ${ct}`);
}
export async function svgToPng(svg) {
    const resvg = new Resvg(svg, {
        // logLevel: 'debug',
        font: {
            loadSystemFonts: false,
        },
        textRendering: 1,
    });
    return resvg.render().asPng();
}
export async function encodePng(input, width, height) {
    return await sharp(input).resize(width, height, { fit: IMAGE_RESIZE_FIT }).png().toBuffer();
}
export async function encodeJpeg(input, width, height, maxBytes) {
    console.log('encode_jpeg', { width, height, maxBytes });
    const resized = await sharp(input).resize(width, height, { fit: IMAGE_RESIZE_FIT }).toBuffer();
    const jpegConfig = config.image.jpeg;
    const jpegOptions = {
        mozjpeg: true,
        chromaSubsampling: '4:2:0',
    };
    if (maxBytes == null) {
        return await sharp(resized)
            .jpeg({
            quality: jpegConfig.defaultQuality,
            ...jpegOptions,
        })
            .toBuffer();
    }
    for (let quality = jpegConfig.defaultQuality; quality >= jpegConfig.minQuality; quality -= jpegConfig.step) {
        const output = await sharp(resized)
            .jpeg({
            quality,
            ...jpegOptions,
        })
            .toBuffer();
        const size = output.length;
        // logger.debug({ msg: 'jpeg_attempt', quality, size })
        if (size <= maxBytes) {
            return output;
        }
    }
    throw new Error(`Unable to encode JPEG under ${maxBytes} bytes (min quality reached)`);
}
