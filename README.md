# The World in One Page — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/h05meigames2/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/h05meigames2/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single original front page summing up the world's news of **Tuesday 24 November 2026** — a 1024×1024 PNG drawn procedurally with Pillow (no photos, no copied artwork).

Lead story: **Jensen Huang is back at Nvidia** — the board reinstates him as CEO 11 days after he quit, shares jump a third and the Nasdaq rallies 6%. Below it, nine story panels cover NATO sending an AWACS aircraft to Poland after three Russian missiles land on its soil, the search resuming at Indonesia's burnt candy factory, Sudan drone strikes near Khartoum, the India–Nepal deals and new cross-border train, Seoul naming a new foreign minister and spy chief, Armenia drafting a new constitution, Dhaka vowing to arrest Sheikh Hasina, Verstappen's Las Vegas Grand Prix win, and the India–New Zealand Test ending in a draw — plus an "Also today" ticker with eleven more stories from Trump's warning to Iran to Pakistan's petrol price cut.

## Run

```sh
python3 gen_image.py   # renders entry.png (1024x1024, deterministic)
python3 main.py        # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

Requirements: Python 3 and Pillow. DejaVu fonts are used when present on the system, otherwise Pillow's default font. No network access; two runs produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).

---

Built for the [make.fun](https://make.fun/?ref=77v1ce78&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) bounty **news-image-20261124** ($100).
