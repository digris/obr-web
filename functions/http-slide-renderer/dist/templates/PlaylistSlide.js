import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { getContrastColor, getImageUrl } from './utils.js';
export function PlaylistSlide({ name, image, editor }) {
    const size = 440;
    const imageUrl = image ? getImageUrl(image.path, size, size) : undefined;
    // const editorImageUrl = editor?.image ? getImageUrl(editor.image.path, size, size) : undefined
    const editorImageUrl = undefined;
    const bgColor = image?.rgb ?? [0, 0, 0];
    const fgColor = getContrastColor(bgColor);
    console.log('playlist_slide', { name, imageUrl, bgColor, fgColor, editor });
    return (_jsx("div", { style: {
            display: 'flex',
            width: '100%',
            height: '100%',
            backgroundColor: `rgb(${bgColor.join(' ')})`,
            color: `rgb(${fgColor.join(' ')})`,
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: 'IBMPlexSans, sans-serif',
        }, children: _jsxs("div", { style: {
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 16,
            }, children: [imageUrl ? (_jsx("img", { src: imageUrl, alt: name, style: {
                        width: size,
                        height: size,
                        objectFit: 'cover',
                        borderRadius: 2,
                        boxShadow: `2px 2px 8px 6px rgba(0, 0, 0, 0.1)`,
                    } })) : (_jsx("div", { style: {
                        width: size,
                        height: size,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: 16,
                    }, children: _jsxs("svg", { xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 602 602", stroke: `rgb(${fgColor.join(' ')})`, strokeWidth: 28, fill: "none", width: size - 64, height: size - 64, children: [_jsx("polygon", { points: "539 301 138 486.99 138 115.01 539 301" }), _jsx("rect", { x: "138.01", y: "107", width: "119.01", height: "387.98" }), _jsx("rect", { x: "345.01", y: "106.99", width: "119.01", height: "387.98" }), _jsx("circle", { cx: "301", cy: "301", r: "287" })] }) })), editorImageUrl && (_jsx("img", { src: editorImageUrl, style: {
                        position: 'absolute',
                        bottom: 16,
                        right: 16,
                        width: Math.round(size * 0.5),
                        height: Math.round(size * 0.5),
                        borderRadius: 9999,
                        objectFit: 'cover',
                        border: '4px solid white',
                    } }))] }) }));
}
