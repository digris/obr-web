import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { getContrastColor } from './utils.js';
export function LogoSlide({ rgb }) {
    const size = 440;
    const bgColor = rgb ?? [0, 0, 0];
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
        }, children: _jsx("div", { style: {
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 16,
            }, children: _jsx("div", { style: {
                    width: size,
                    height: size,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: 16,
                }, children: _jsxs("svg", { xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 602 602", stroke: `rgb(${fgColor.join(' ')})`, strokeWidth: 28, fill: "none", width: size - 64, height: size - 64, children: [_jsx("polygon", { points: "539 301 138 486.99 138 115.01 539 301" }), _jsx("rect", { x: "138.01", y: "107", width: "119.01", height: "387.98" }), _jsx("rect", { x: "345.01", y: "106.99", width: "119.01", height: "387.98" }), _jsx("circle", { cx: "301", cy: "301", r: "287" })] }) }) }) }));
}
