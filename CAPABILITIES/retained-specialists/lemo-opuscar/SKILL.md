---
name: lemo-opuscar
description: Direct and produce short films made entirely in code across 67 styles (Canvas, WebGL, 2D/3D). Features algorithmic frame-by-frame rendering, Kokoro TTS voice, procedural audio, and director guidelines.
---

# Lemo-Opuscar

Lemo-Opuscar is an algorithmic film directing and production toolbox that generates animated short films, documentary shorts, explainers, and motion graphics entirely from code. There is zero video generation and zero stock footage; every frame is drawn deterministically in Canvas or WebGL, scored with procedural audio and sample libraries, narrated with neural text-to-speech, and mixed to broadcast audio standards.

## Workflow

### 1. Take the Brief and Select a Style
Directing starts with understanding the user's intent:
- **Style Selection:** Name a style in English or Chinese (e.g. *Watercolor Brush* / 水彩笔刷, *Ukiyo-e* / 浮世绘, *Swiss Motion Graphics* / 瑞士动态排版, *Satellite Briefing* / 卫星简报, *Exploded Teardown* / 产品拆解). Inspect the complete [styles catalogue](references/styles.md).
- **Format Defaults:** 30–60 seconds, 1920×1080 at 24 fps (or style default), burned-in captions + `.srt`, loudness −14 LUFS.
- **One Question Round:** Ask only once upfront about must-have shots, custom brand assets, voice preferences, or whether they want to inspect key storyboard frames first.

### 2. Directing & Narrative Structure
Consult the core [director guide](references/director.md) before writing any code:
- **Narrative Arc:** One subject, one goal, one turn. Hook the viewer in the first 3 seconds.
- **Native Medium Move:** Identify the signature transition that only this visual medium can achieve (e.g. wet ink blooming into the next scene, an isometric blueprint folding into a model, a Swiss type grid snapping into a logo).
- **Sound-Led Rhythm:** Cut visuals to the soundtrack. Generate voice narration and score stems first to establish the authoritative timeline.

### 3. Technical Pipeline & Frame Function
Follow the technical specification in [technique guide](references/technique.md):
- **Deterministic Frame Rendering:** Every film exposes a single HTML entry point with:
  ```js
  window.DUR = 45.0;              // Duration in seconds
  window.render = (t) => { ... }; // Draw frame at time t (seconds)
  window.READY = true;            // Signaled after font and texture loads
  ```
- **Voice Narration:** Synthesize spoken narration using Kokoro TTS (English, offline) or Edge TTS (Chinese) and verify timestamps with Whisper.
- **Music & Foley:** Generate procedural audio events synchronized to visual collision timestamps.
- **Mastering & Mixing:** Balance dialogue, foley, and score. Duck music by −8 dB under speech. Two-pass FFmpeg `loudnorm` target: −14 LUFS, −1 dBTP.

### 4. Agent Workflow & Execution Rules
Review the operational requirements in [agents guide](references/agents.md):
- Write `TREATMENT.md` defining shot breakdown, voice lines, sound cues, and visual benchmarks.
- Render key frames with headless Chrome: `node core/render/still.mjs <project> <time>`.
- Build the full video: `sh build.sh` compiles frames and multiplexes audio into `film.mp4`.

### 5. Customizing and Creating Styles
To modify an existing library style or build an original visual language from a blank canvas, follow the five-step process documented in [my-styles guide](references/my-styles.md):
- Isolate safe attributes (palette, type, pacing) from core character (rendering engine, camera grammar).
- Test one comparison style frame before generating a full demo film.
- Persist custom styles in `~/lemo-my-styles/<name>/`.

## Offline Style & Director Lookup

Query available film styles, categories, and director principles from the terminal:
```bash
# List film styles by category
python3 -B scripts/style_lookup.py --list evidence

# Search styles by keyword
python3 -B scripts/style_lookup.py --search ukiyoe

# Inspect full details for a specific style
python3 -B scripts/style_lookup.py --style swiss-motion

# Print director rules summary
python3 -B scripts/style_lookup.py --rules
```

## Attribution & Provenance
Lemo-Opuscar is created by LemoLab ([lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)) and licensed under the MIT License.
Preserved upstream snapshot commit: `bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00`.
Integrated into GraviDex under strict zero-emoji governance with pure standard library tooling.

