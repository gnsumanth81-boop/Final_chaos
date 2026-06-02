import { createReadStream, existsSync } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../public/", import.meta.url));
const port = Number(process.argv[2] ?? process.env.PORT ?? 4173);

const types = {
  ".html": "text/html; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml"
};

function safePath(urlPath) {
  const pathname = decodeURIComponent(urlPath.split("?")[0]);
  const clean = normalize(pathname)
    .replace(/^[/\\]+/, "")
    .replace(/^(\.\.[/\\])+/, "");
  const resolved = join(root, clean === "" ? "index.html" : clean);
  return resolved.startsWith(root) ? resolved : join(root, "index.html");
}

createServer(async (req, res) => {
  const file = safePath(req.url ?? "/");
  const target = existsSync(file) ? file : join(root, "index.html");
  try {
    const info = await stat(target);
    if (!info.isFile()) throw new Error("Not a file");
    res.writeHead(200, {
      "Content-Type": types[extname(target)] ?? "application/octet-stream",
      "Cache-Control": "no-store"
    });
    createReadStream(target).pipe(res);
  } catch {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not found");
  }
}).listen(port, "127.0.0.1", () => {
  console.log(`Chaos dashboard: http://127.0.0.1:${port}`);
});
