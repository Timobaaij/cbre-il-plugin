# cbre-il

CBRE skills for Claude Code and Cowork, packaged as a plugin.

## Skills

| Skill | What it does |
|-------|--------------|
| `cbre-corporate-pptx` | Build CBRE-branded PowerPoint decks |
| `cbre-il-account-briefing` | Build IL account briefing decks |
| `cbre-property-longlist` | Build interactive property longlist dashboards |
| `cbre-tone-of-voice` | Write in the CBRE voice |

Each is available as `/cbre-il:<skill-name>` once the plugin is installed, and
Claude auto-invokes them based on each skill's `description`.

## Layout

```
plugins/cbre-il/
├── .claude-plugin/
│   └── plugin.json          # plugin manifest (name, version, author)
└── skills/
    └── <skill-name>/
        └── SKILL.md         # one folder per skill (+ its supporting files)
```

## Adding a skill

1. Create a folder under `skills/` named in kebab-case (e.g. `skills/lease-abstraction/`).
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) and markdown
   instructions in the body. The `description` is what Claude uses to decide when
   to auto-invoke the skill — make it specific about *when* to use it. If it
   contains a colon-space, quote it or use a `>-` block scalar.

## Versioning

Bump `version` in `.claude-plugin/plugin.json` (and the matching entry in the
repo's `.claude-plugin/marketplace.json`) whenever you ship changes. Installed
users only pull updates when the version changes.
