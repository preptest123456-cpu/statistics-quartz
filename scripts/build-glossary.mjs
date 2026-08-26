#!/usr/bin/env node
/**
 * Regenerates `content/glossary/` from the concept wikilinks used in the chapter notes.
 *
 * The chapter notes were generated from a PDF and are full of `[[concept]]` links that
 * never had a target note, which made them dead links on the built site. This script
 * creates one hub note per concept, recording which chapters reference it, so those
 * links resolve. Nothing here invents statistical content: every note is derived from
 * links that already exist in the vault.
 *
 * Run with: npm run glossary
 */
import fs from "node:fs"
import path from "node:path"

const CONTENT = "content"
const GLOSSARY = path.join(CONTENT, "glossary")
const WIKILINK = /(!?)\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]/g

/** Mirrors Quartz's `sluggify` (quartz/util/path.ts) — case-preserving. */
const sluggify = (s) =>
  s.replace(/\s/g, "-").replace(/&/g, "-and-").replace(/%/g, "-percent").replace(/[?#]/g, "")

/** Key used to merge spelling variants ("F distribution" / "F-distribution") into one note. */
const conceptKey = (s) => sluggify(s).toLowerCase().replace(/_/g, "-")

const chapterFiles = fs
  .readdirSync(CONTENT)
  .filter((f) => f.endsWith(".md") && f !== "index.md")
  .sort()

const noteTitle = (basename) => {
  const src = fs.readFileSync(path.join(CONTENT, `${basename}.md`), "utf8")
  const fm = src.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  const title = fm?.[1]
    .match(/^title:\s*(.+)$/m)?.[1]
    ?.trim()
    .replace(/^["']|["']$/g, "")
  return title || basename.replace(/_/g, " ")
}

const existing = new Set(chapterFiles.map((f) => f.replace(/\.md$/, "")).concat("index"))
const titles = Object.fromEntries(
  [...existing].filter((b) => b !== "index").map((b) => [b, noteTitle(b)]),
)

// term key -> { variants: Map<variant, count>, chapters: Set<basename> }
const concepts = new Map()
for (const file of chapterFiles) {
  const basename = file.replace(/\.md$/, "")
  for (const m of fs.readFileSync(path.join(CONTENT, file), "utf8").matchAll(WIKILINK)) {
    if (m[1] === "!") continue // embeds are not concept links
    const target = m[2].trim()
    if (existing.has(target)) continue // links between chapter notes are already fine
    const key = conceptKey(target)
    if (!concepts.has(key)) concepts.set(key, { variants: new Map(), chapters: new Set() })
    const entry = concepts.get(key)
    entry.variants.set(target, (entry.variants.get(target) ?? 0) + 1)
    entry.chapters.add(basename)
  }
}

/** Most-used spelling wins; ties break toward the longer, then alphabetically stable, form. */
const canonicalOf = (variants) =>
  [...variants.entries()].sort(
    (a, b) => b[1] - a[1] || b[0].length - a[0].length || a[0].localeCompare(b[0]),
  )[0][0]

fs.rmSync(GLOSSARY, { recursive: true, force: true })
fs.mkdirSync(GLOSSARY, { recursive: true })

const written = []
for (const [key, { variants, chapters }] of concepts) {
  const canonical = canonicalOf(variants)
  // Quartz resolves a wikilink by slug, so the filename must slugify to the linked text.
  const filename = `${sluggify(canonical)}.md`
  // Any other spelling needs an alias so its slug resolves here too.
  const aliases = [...variants.keys()].filter((v) => sluggify(v) !== sluggify(canonical))

  const sortedChapters = [...chapters].sort((a, b) => a.localeCompare(b))
  const frontmatter = [
    "---",
    `title: ${JSON.stringify(canonical)}`,
    ...(aliases.length ? ["aliases:", ...aliases.map((a) => `  - ${JSON.stringify(a)}`)] : []),
    "tags:",
    "  - glossary",
    "---",
  ].join("\n")

  const body = [
    "",
    `# ${canonical}`,
    "",
    "> [!abstract] Concept note",
    "> This is a stub linking the chapters that discuss this concept. Add your own definition here.",
    "",
    "## Discussed in",
    "",
    ...sortedChapters.map((c) => `- [[${c}|${titles[c]}]]`),
    "",
    "---",
    "",
    "[[glossary/index|← Back to the glossary]]",
    "",
  ].join("\n")

  fs.writeFileSync(path.join(GLOSSARY, filename), frontmatter + body, "utf8")
  written.push({ key, canonical, aliases, chapters: sortedChapters.length })
}

written.sort((a, b) => a.canonical.toLowerCase().localeCompare(b.canonical.toLowerCase()))

// Alphabetical index page.
const groups = new Map()
for (const w of written) {
  const letter = /^[A-Za-z]/.test(w.canonical) ? w.canonical[0].toUpperCase() : "#"
  if (!groups.has(letter)) groups.set(letter, [])
  groups.get(letter).push(w)
}

const indexLines = [
  "---",
  'title: "Glossary"',
  "tags:",
  "  - glossary",
  "---",
  "",
  "# Glossary",
  "",
  `${written.length} concepts referenced across the chapter notes.`,
  "Each entry lists the chapters that discuss it; definitions are yours to fill in.",
  "",
  "> [!note] Generated file",
  "> This folder is rebuilt by `npm run glossary`. Add definitions to the individual",
  "> concept notes — but note that re-running the script overwrites them.",
  "",
]
for (const letter of [...groups.keys()].sort()) {
  indexLines.push(`## ${letter}`, "")
  for (const w of groups.get(letter))
    indexLines.push(`- [[${sluggify(w.canonical)}|${w.canonical}]]`)
  indexLines.push("")
}
fs.writeFileSync(path.join(GLOSSARY, "index.md"), indexLines.join("\n"), "utf8")

const aliasCount = written.reduce((s, w) => s + w.aliases.length, 0)
console.log(`Wrote ${written.length} concept notes (+${aliasCount} aliases) to ${GLOSSARY}`)
