const PATH_REGEX = /^\/render\/(?<ct>[a-z0-9_-]+):(?<uid>[A-Z0-9]{8})\/(?<width>\d+)x(?<height>\d+)\.(?<format>jpg|png|webp)$/i;
export function parseRequest(path) {
    // normalize trailing slash
    path = path.replace(/\/+$/, "");
    const match = path.match(PATH_REGEX);
    if (!match?.groups) {
        throw new Error("Invalid path");
    }
    const { ct, uid, width, height, format } = match.groups;
    return {
        ct,
        uid,
        width: Number(width),
        height: Number(height),
        format: format,
    };
}
