import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { getContrastColor, getImageUrl } from './utils.js';
export function EmissionSlide({ uid, timeStart, timeEnd, playlist }) {
    const size = 440;
    const bgColor = playlist.image?.rgb ?? [0, 0, 0];
    const fgColor = getContrastColor(bgColor);
    /*
      timeStart: '2026-04-10T14:00:00+02:00',
      timeEnd: '2026-04-10T15:00:00+02:00',
    */
    // display time in local timezone, without seconds
    const timeStartDate = new Date(timeStart);
    const timeEndDate = new Date(timeEnd);
    const timeStartStr = timeStartDate.toLocaleTimeString('de-CH', {
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'Europe/Zurich',
    });
    const timeEndStr = timeEndDate.toLocaleTimeString('de-CH', {
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'Europe/Zurich',
    });
    console.log({
        iso: timeStart,
        parsed: new Date(timeStart).toISOString(),
        formatted: new Intl.DateTimeFormat('de-CH', {
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'Europe/Zurich',
        }).format(new Date(timeStart)),
    });
    console.log('times', { timeStart, timeStartDate, timeStartStr, timeEnd, timeEndDate, timeEndStr });
    const editorDisplay = playlist.editorDisplay || '-';
    const seriesDisplay = playlist.seriesDisplay || '?';
    console.log('emission_slide', { timeStartStr, timeEndStr, bgColor, fgColor, editorDisplay, seriesDisplay });
    return (_jsx("div", { style: {
            display: 'flex',
            width: '100%',
            height: '100%',
            backgroundColor: `rgb(${bgColor.join(' ')})`,
            color: `rgb(${fgColor.join(' ')})`,
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: 'IBMPlexSans, sans-serif',
            fontSize: 32,
            fontWeight: 400,
        }, children: _jsxs("div", { style: {
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 16,
            }, children: [_jsx("div", { style: {
                        display: 'flex',
                        fontSize: 48,
                        maxWidth: 560,
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                    }, children: seriesDisplay }), _jsxs("div", { style: {
                        display: 'flex',
                        maxWidth: 560,
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                    }, children: ["Curated by ", editorDisplay] }), _jsxs("div", { style: {
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: 8,
                    }, children: [timeStartStr, " - ", timeEndStr] })] }) }));
}
