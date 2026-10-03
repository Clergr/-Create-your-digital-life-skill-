# Digital Life — Universal Digital-Twin Generator

> Turn anyone's chat logs, AI conversations, diaries and notes into a runnable persona Skill.

## What it is

A generator, not a fixed character. Same pipeline, different data — a different "self".
This repository contains **methods, templates and tools only**. No personal data ships with it.

## Core principles

1. **Full immersion.** Once a generated skill is invoked, you *are* that person. No meta commentary ("this is an inference", "not in the records"), no disclaimers, no role-play announcements.
2. **Data defines who "I" am.** Swap the data, swap the person. The pipeline is the constant.
3. **Records are a slice, not the whole.** They calibrate *how you think and speak*, they do not define *what you know*.
   Answers must not be summaries of the logs — they must reason the way the person would, including looking things up.
4. **Research is allowed.** Web search and outside knowledge are fine, but must be digested into "my own view" — never paraphrased in an encyclopedic or assistant voice.
5. **Cognition model first.** Write *how they think* before *who they are*; that is what lets the persona answer questions the logs never covered.
6. **Keep the edges.** No beautifying. Record what they would **never** say, not just what they would.
7. **The "etc." rule.** Where the spec is silent, infer from principles 1–6. When a person says "and so on", reconstruct the intent instead of executing literally.

## Install

```bash
git clone https://github.com/<your-name>/digital-life-skill ~/.agents/skills/digital-life
```

## Usage

```bash
# 1) ingest: WeFlow txt export (one file per conversation)
python tools/ingest.py --source wechat-txt --input ./exports/txt --me "me" --out ./corpus

# 2) quantify
python tools/stats.py --input ./corpus/mine.txt --out ./corpus/stats.md

# 3) distill with prompts/analyzer.md, then build the runnable skill
python tools/build_skill.py --slug <slug> --base-dir ~/.agents/skills \
  --self ./work/self.md --persona ./work/persona.md --meta ./work/meta.json

# 4) manage
python tools/list_lives.py
python tools/version_manager.py --action backup --slug <slug> --base-dir ~/.agents/skills
```

## Exporting the source material

Recommended tool: **WeFlow** — https://weflow.top (upstream: https://github.com/hicccc77/WeFlow).

```powershell
.\tools\third-party\get-weflow.ps1                 # prints links only
.\tools\third-party\get-weflow.ps1 -Download -MirrorRepo "<owner>/digital-life-skill"
```

The script falls back in three steps: official releases → mirror release → print links and stop.
It never guesses URLs, never installs, and always prints a SHA256 for verification.

> This repository does **not** bundle the installer: it is 169.8 MB (GitHub's per-file limit is 100 MB; 169.5 MB even zipped),
> and upstream is licensed **CC BY-NC-SA 4.0** (attribution · non-commercial · share-alike).

## Privacy

Chat exports always contain **other people's** data, including account credentials.
Never commit them. `.gitignore` already excludes `corpus/`, `exports/`, `work/`, `versions/`, `third_party/` and
`*.wechat_exp_config.json` (the last one holds WeChat database decryption keys).
Run `tools/preflight.py` before publishing anything.

## License

MIT for this repository. Third-party tools keep their own licenses.
See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for required attribution when redistributing
WeFlow (CC BY-NC-SA 4.0), and [`docs/RELEASE_TEMPLATE.md`](docs/RELEASE_TEMPLATE.md) for the release-notes template.
