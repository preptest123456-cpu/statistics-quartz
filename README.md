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
checks its links, and publishes to GitHub Pages.

> The other workflows (`ci.yaml`, `build-preview.yaml`, `deploy-preview.yaml`,
> `docker-build-push.yaml`) came from upstream Quartz and are gated on
> `github.repository == 'jackyzha0/quartz'`, so they never run here.
> `site-check.yml` is the one that runs on pull requests in this fork.

## Upstream

Quartz is by [jackyzha0](https://github.com/jackyzha0/quartz), MIT licensed — see
`LICENSE.txt`. To pull in upstream changes, merge `v4` from the Quartz remote and keep
your `content/`, `quartz.config.ts`, and `quartz.layout.ts`.
