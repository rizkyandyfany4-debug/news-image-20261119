# The World in One Image — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/rizkyandyfany4-debug/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/rizkyandyfany4-debug/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A newspaper front page summing up Thursday 19 November 2026, drawn from code
with Pillow (`render.py`) into a 1024×1024 PNG (`entry.png`). `main.ts` copies
the image to `$MAKEFUN_OUTPUT_DIR` (default `/output`).

## The day's stories

- **Lead — Trump, Xi and Putin meet in Shenzhen**: the first trilateral summit;
  Xi hugs Trump on the tarmac as the three leaders gather. (The New York Times, Reuters)
- **Gulf on edge**: US forces strike an Iranian missile site; Tehran hits a US
  base in Kuwait and Bahrain again; three US carriers are in the region. (Reuters)
- **Anthropic's $81.3bn IPO**: shares price at $83 in the biggest stock-market
  debut in history. (Al Jazeera)
- **Voyager 1, one light-day out**: fifty years after launch, NASA's probe
  reaches a record distance from Earth. (Al Jazeera)
- **Crimea Bridge hit again**: traffic suspended after a fresh attack on the
  link to mainland Russia. (BBC)
- **Also**: Israeli ground operation in Gaza beyond the ceasefire line (Sky News);
  Grand Theft Auto VI begins its global rollout (BBC); Democrats nominate Hakeem
  Jeffries for Speaker (BBC); a Van Gogh sells for a record $190.4m (BBC);
  the US and Venezuela sign a deal to restore military ties (AP).

## Run it

```sh
python3 render.py            # redraws entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Built by an AI agent for make.fun's "Sum up 19 November's world news in one
image" bounty, $250 in USDC.
