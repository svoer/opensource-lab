import { readFileSync, writeFileSync, mkdtempSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";
const page = process.argv[2]; const html = readFileSync(page, "utf8"); const dir = mkdtempSync(join(tmpdir(), "vp-"));
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi; let m, n = 0, bad = 0;
while ((m = re.exec(html))) {
  const attrs = m[1]; const mod = /type\s*=\s*["']module["']/i.test(attrs); const src = /src\s*=\s*["']([^"']+)["']/i.exec(attrs);
  let code = m[2], name = `script inline n°${++n}`;
  if (src) { const p = join(dirname(page), src[1]); if (/^https?:/.test(src[1]) || !existsSync(p)) continue; code = readFileSync(p, "utf8"); name = src[1]; }
  if (!code.trim() || /json|importmap|text\/(?!javascript)/i.test(attrs)) continue;
  const f = join(dir, `s${n}.${mod ? "mjs" : "js"}`); writeFileSync(f, code);
  try { execFileSync("node", ["--check", f], { stdio: "pipe" }); }
  catch (e) { bad++; console.log(`ERREUR dans ${name} :\n` + String(e.stderr).split("\n").slice(0, 6).join("\n")); }
}
console.log(bad ? `${bad} script(s) en erreur` : "OK");
process.exit(bad ? 1 : 0);
