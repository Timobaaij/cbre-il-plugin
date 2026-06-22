# cbre-il-plugin

A shareable [Claude Code](https://code.claude.com/docs/en/overview) plugin for
CBRE skills. This repo is **both a plugin and a marketplace**, so colleagues can
add it and install the plugin in two commands.

## Repository layout

```
cbre-il-plugin/
├── .claude-plugin/
│   └── marketplace.json          # the shareable catalog (lists the plugin below)
├── plugins/
│   └── cbre-il/
│       ├── .claude-plugin/
│       │   └── plugin.json        # the plugin manifest
│       ├── skills/
│       │   ├── cbre-corporate-pptx/        # CBRE-branded PowerPoint decks
│       │   ├── cbre-il-account-briefing/   # IL account briefings
│       │   ├── cbre-property-longlist/     # property longlist dashboards
│       │   └── cbre-tone-of-voice/         # CBRE writing voice
│       └── README.md
└── README.md
```

## Install (for your colleagues)

Inside any Claude Code session:

```
/plugin marketplace add timobaaij/cbre-il-plugin
/plugin install cbre-il@cbre
```

- `cbre-il` is the plugin name, `cbre` is the marketplace name (from
  `marketplace.json` → `name`).
- After installing, the plugin's skills appear as `/cbre-il:<skill-name>` and
  Claude can auto-invoke them based on each skill's `description`.

To update later: `/plugin marketplace update cbre` then re-install/enable.

## Add another CBRE skill

1. Create a folder per skill under `plugins/cbre-il/skills/`, named in
   kebab-case (e.g. `skills/lease-abstraction/`), with a `SKILL.md` directly
   inside it.
2. The `SKILL.md` needs YAML frontmatter (`name`, `description`) + markdown
   instructions. The `description` controls *when* Claude uses the skill — be
   specific about the trigger situation and keywords. If the description
   contains a colon followed by a space, quote it or use a `>-` block scalar so
   the YAML stays valid.
3. Bump `version` in both `plugin.json` and `marketplace.json`, then commit and push.

> Note: build artifacts (`__pycache__/`, `*.pyc`, `.pytest_cache/`) don't belong
> in a shared skill — the root `.gitignore` keeps them out of git commits.
> Uploading a folder via the GitHub web UI bypasses `.gitignore`, so zip/commit
> from a clean tree instead.

## Test locally before sharing

```bash
# validate the plugin and marketplace manifests
claude plugin validate ./plugins/cbre-il
claude plugin validate .

# load the plugin in a session without installing it
claude --plugin-dir ./plugins/cbre-il
```

## Docs

- Plugins — https://code.claude.com/docs/en/plugins
- Plugin marketplaces — https://code.claude.com/docs/en/plugin-marketplaces
- Skills — https://code.claude.com/docs/en/skills
