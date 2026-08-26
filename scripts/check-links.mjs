#!/usr/bin/env node
/**
 * Fails if the built site contains internal links that go nowhere.
 *
 * Two failure modes are reported:
 *   1. Unresolved wikilinks. With `disableBrokenWikilinks` on, Quartz renders a
 *      wikilink with no matching note as `<a class="internal broken">` — readable,
 *      but a dead end the author probably did not intend.
 *   2. Dangling hrefs. Any other internal link whose target is missing from the
 *      build output, which would 404 for a reader.
 *
 * Usage: node scripts/check-links.mjs [outputDir]   (default: public)
 */
import fs from "node:fs"
import path from "node:path"

const root = process.argv[2] ?? "public"
if (!fs.existsSync(root)) {
  console.error(`No build output at "${root}". Run \`npx quartz build\` first.`)
  process.exit(2)
}

const files = []
const walk = (dir) => {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name)
    entry.isDirectory() ? walk(p) : files.push(p)
  }
}
walk(root)

const rel = (f) =>
  f
    .slice(root.length + 1)
    .split(path.sep)
    .join("/")
const htmlFiles = files.filter((f) => f.endsWith(".html"))
const pages = new Set(htmlFiles.map((f) => rel(f).replace(/\.html$/, "")))
const assets = new Set(files.map(rel))

// `href` and `class` appear in either order depending on the emitter.
const ANCHOR = /<a\b[^>]*>/g
const HREF = /\bhref="([^"]*)"/
const INTERNAL = /\bclass="[^"]*\binternal\b[^"]*"/

// `<a class="internal broken">Label</a>` — a wikilink Quartz could not resolve.
const UNRESOLVED = /<a\b[^>]*\bclass="[^"]*\bbroken\b[^"]*"[^>]*>([\s\S]*?)<\/a>/g

const broken = new Map()
const unresolved = new Map()
for (const file of htmlFiles) {
  const from = rel(file).replace(/\.html$/, "")
  const fromDir = path.posix.dirname(from)
  const html = fs.readFileSync(file, "utf8")

  for (const m of html.matchAll(UNRESOLVED)) {
    const label = m[1].replace(/<[^>]*>/g, "").trim() || "(empty)"
    if (!unresolved.has(label)) unresolved.set(label, new Set())
    unresolved.get(label).add(from)
  }

  for (const [tag] of html.matchAll(ANCHOR)) {
    if (!INTERNAL.test(tag)) continue
    const href = tag.match(HREF)?.[1]
    if (!href) continue
    const target = href.split("#")[0].split("?")[0]
    // Protocol-relative, absolute-scheme, and pure-anchor links are out of scope.
    if (!target || target.startsWith("//") || /^[a-z][a-z0-9+.-]*:/i.test(target)) continue
    const resolved = path.posix.normalize(path.posix.join(fromDir, target)).replace(/\/$/, "")
    // A link to a directory (e.g. href=".") is served by that directory's index.
    const candidates = [resolved, `${resolved}/index`, resolved === "." ? "index" : null]
    if (candidates.some((c) => c && (pages.has(c) || assets.has(c)))) continue
    if (!broken.has(resolved)) broken.set(resolved, new Set())
    broken.get(resolved).add(from)
  }
}

const report = (title, entries) => {
  const total = [...entries.values()].reduce((sum, s) => sum + s.size, 0)
  console.error(`\n✗ ${total} ${title} (${entries.size} distinct):\n`)
  for (const [target, sources] of [...entries.entries()].sort((a, b) => b[1].size - a[1].size)) {
    console.error(`  ${target}`)
    for (const s of [...sources].sort().slice(0, 5)) console.error(`      from ${s}`)
    if (sources.size > 5) console.error(`      ...and ${sources.size - 5} more`)
  }
}

if (broken.size === 0 && unresolved.size === 0) {
  console.log(`✓ No dead internal links across ${htmlFiles.length} pages.`)
  process.exit(0)
}

if (unresolved.size > 0) report("unresolved wikilink(s)", unresolved)
if (broken.size > 0) report("dangling internal link(s)", broken)
console.error(
  "\nFix by creating the missing note, correcting the link, or re-running `npm run glossary`.",
)
process.exit(1)
