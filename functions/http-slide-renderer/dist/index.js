import { http } from "@google-cloud/functions-framework";
import { parseRequest } from "./parser.js";
function render(req, res) {
    try {
        const parsed = parseRequest(req.path);
        console.log("render_request", parsed);
        res.set("Content-Type", "application/json");
        res.status(200).send(parsed);
    }
    catch (err) {
        const message = err instanceof Error ? err.message : "Unknown error";
        console.warn("render_error", {
            path: req.path,
            error: message,
        });
        res.status(400).send({ error: message });
    }
}
// 👇 THIS is the key line for dev mode
http("render", render);
