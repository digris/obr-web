import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { getContrastColor, getImageUrl } from './utils.js';
export function MediaSlide({ name, artistDisplay, releases }) {
    const image = releases.find((r) => r.image)?.image;
    const size = 400;
    const imageUrl = image ? getImageUrl(image.path, size, size) : undefined;
    const bgColor = image?.rgb ?? [0, 0, 0];
    const fgColor = getContrastColor(bgColor);
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
                        width: 320,
                        height: 320,
                        objectFit: 'cover',
                        borderRadius: 2,
                        boxShadow: `2px 2px 8px 6px rgba(0, 0, 0, 0.1)`,
                    } })) : (_jsx("div", { style: {
                        width: 320,
                        height: 320,
                        backgroundColor: '#333',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        borderRadius: 2,
                    }, children: "No Image" })), _jsxs("div", { style: {
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        textAlign: 'center',
                        gap: 2,
                    }, children: [_jsx("p", { style: {
                                fontSize: 28,
                                fontWeight: 600,
                                margin: 0,
                                maxWidth: 560,
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                            }, children: name }), _jsx("p", { style: {
                                fontSize: 28,
                                margin: 0,
                                maxWidth: 560,
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                            }, children: artistDisplay })] })] }) }));
}
