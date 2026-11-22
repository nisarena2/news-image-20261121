# World News in One Image — 21 November 2026

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/nisarena2/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/nisarena2/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One front-page image summing up Saturday, 21 November 2026's world news.

**Lead story:** Trump, Xi and Putin meet in Shenzhen at the APEC trilateral
summit, agreeing to nuclear-risk talks.

**Also in the picture:**

- Russia hits Kyiv bridges; missiles cross into Polish airspace — NATO calls
  it a grave violation
- Saudi defences down 3 Houthi missiles over Riyadh
- AI sell-off sinks markets — S&P and Dow fall into correction (S&P −3.7%)
- COP31 climate talks run into a second day of overtime over fossil fuels
- ICJ rules on Myanmar in the Rohingya genocide case
- Cancer pill breakthrough — daraxonrasib leaves tumours undetectable in
  1 in 12 patients

## How it is made

`draw.py` draws the image from scratch with Pillow (flat editorial
illustration, DejaVu fonts) and writes `entry.png`. `main.py` copies that
image to the output directory as `entry.png` — the same bytes every run.
