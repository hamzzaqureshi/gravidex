# How to Share the GraviDex Skills Suite

This guide explains how to share the GraviDex modular skills with friends, teammates, and the developer community.

---

## Method 1: Send the Ready-Made ZIP (Fastest)

If your friends just want a file to download via **Discord, WhatsApp, Telegram, Slack, or Google Drive**:

1. A clean, self-contained ZIP archive is generated in your `dist/` folder:
   - **File:** `dist/gravidex.zip`
2. Send this file to your friend.
3. **Instructions for your friend:**
   - Unzip the file anywhere.
   - Open terminal in the unzipped folder and run:
     ```bash
     # Linux / macOS:
     ./install.sh

     # Windows (Command Prompt / PowerShell):
     python install.py
     ```
   - The interactive prompt lets them choose:
     - `1) Antigravity Global` (`~/.gemini/config/skills`) — skills become available in all their projects.
     - `2) Current Project Workspace` (`./.agents/skills`) — skills are scoped to that project.
     - `3) OpenCode Global` (`~/.config/opencode/skills`) — for friends using OpenCode.
     - `4) Claude Code Global` (`~/.claude/skills`) — for friends using Claude Code CLI.

> **Tip:** You can re-generate fresh ZIP archives anytime by running:
> ```bash
> python3 -B package.py
> ```

---

## Method 2: Share via GitHub

The official repository is hosted at [https://github.com/hamzzaqureshi/gravidex](https://github.com/hamzzaqureshi/gravidex).

### How Friends Install from Your GitHub Repo:
```bash
git clone https://github.com/hamzzaqureshi/gravidex.git
cd gravidex
./install.sh
```

### How Friends Add Skills to Their Existing Projects (Git Submodule):
```bash
# In their project directory:
git submodule add https://github.com/hamzzaqureshi/gravidex.git .agents/skills
```

---

## Method 3: Safe Web Installer (Zero-Clone)

Friends can download and run the verified installer directly:

```bash
curl -fsSL https://raw.githubusercontent.com/hamzzaqureshi/gravidex/main/install.sh -o /tmp/gravidex-install.sh && bash /tmp/gravidex-install.sh
```

To install directly to their global configuration without prompts:
```bash
curl -fsSL https://raw.githubusercontent.com/hamzzaqureshi/gravidex/main/install.sh -o /tmp/gravidex-install.sh && bash /tmp/gravidex-install.sh --global
```

Or install specific capabilities:
```bash
curl -fsSL https://raw.githubusercontent.com/hamzzaqureshi/gravidex/main/install.sh -o /tmp/gravidex-install.sh && bash /tmp/gravidex-install.sh --skills autonomous-agent-engineering,design-systems,boardui --global
```

---

## Method 4: As an Antigravity Plugin

Antigravity natively supports modular **Plugins** (`plugins/<plugin-name>/plugin.json`).

When you run `python3 -B package.py`, it automatically generates:
`dist/gravidex-pack/`

Friends can drop this folder directly into their Antigravity plugins directory:
- **Global:** `~/.gemini/config/plugins/gravidex-pack/`
- **Project:** `<project-root>/.agents/plugins/gravidex-pack/`

Antigravity auto-discovers and loads all skills immediately with zero configuration required.
