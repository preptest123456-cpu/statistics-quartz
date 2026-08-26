# Statistics Notes

An Obsidian vault of statistics chapter notes, published as a website with
[Quartz v4](https://quartz.jzhao.xyz/).

**Live site:** https://preptest123456-cpu.github.io/statistics-quartz

## What's in here

| Path                | Contents                                                              |
| ------------------- | --------------------------------------------------------------------- |
| `content/`          | The Obsidian vault — 18 chapter notes and 2 appendices                |
| `content/glossary/` | Generated concept notes, one per term linked from the chapters        |
| `quartz/`           | The Quartz static site generator (upstream, generally left untouched) |
| `quartz.config.ts`  | Site title, base URL, plugins                                         |
| `quartz.layout.ts`  | Which components appear where on the page                             |
| `scripts/`          | Repo-specific tooling (glossary generator, link checker)              |
| `docs/`             | Upstream Quartz documentation, kept for reference                     |

## Working locally

```bash
npm ci                     # once
npx quartz build --serve   # preview at http://localhost:8080
```

Edit `content/` in Obsidian; the dev server rebuilds on save.

## Before you push

```bash
npm run verify   # build the site, then fail on any dead internal link
```

The same check runs in CI and on every deploy.

## Companion notebooks

Chapters 14 and 15 have worked examples in Jupyter, kept in
[statistics-jupyter](https://github.com/preptest123456-cpu/statistics-jupyter). Each of
those chapter pages opens with a callout linking straight to Colab, GitHub, and a
download — the data is inline, so they run in the browser with no setup.

To add one for another chapter: drop the notebook in that repo under `notebooks/`, then
copy the callout from the top of `content/Chapter_14_Simple_Linear_Regression.md` and
swap the filename.

## The glossary

The chapter notes link concepts with wikilinks (`[[standard deviation]]`) that had no
target notes, so every one of them was a dead link on the site. `content/glossary/`
fills that gap: one note per concept, listing the chapters that discuss it.

```bash
npm run glossary   # regenerate from the wikilinks currently in content/
```

The notes are scaffolds — they carry no definitions, only the cross-references derived
from the vault. Write definitions into them as you study, but be aware that re-running
the generator **overwrites the folder**. Once you start adding real content, either stop
running it or move edited notes out of `content/glossary/`.

## Deploying

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site,
checks its links, and publishes to GitHub Pages. `site-check.yml` runs the same build
and link check on pull requests and other branches.

Those two are the only workflows here. The upstream Quartz ones (`ci.yaml`,
`build-preview.yaml`, `deploy-preview.yaml`, `docker-build-push.yaml`) were gated on
`github.repository == 'jackyzha0/quartz'` and could never run on this fork, so they were
removed along with upstream's funding, issue, and PR templates, its code of conduct, and
the Dockerfile. All of it remains in git history if you want any of it back.

## Upstream

Quartz is by [jackyzha0](https://github.com/jackyzha0/quartz), MIT licensed — see
`LICENSE.txt`. To pull in upstream changes, merge `v4` from the Quartz remote and keep
your `content/`, `quartz.config.ts`, and `quartz.layout.ts`.
