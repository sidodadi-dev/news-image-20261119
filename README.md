# The World in One Day — Thursday 19 November 2026

An entry for make.fun's **"Sum up 19 November's world news in one image"**
bounty. One picture, the whole day:

- **Shenzhen** — Trump, Xi and Putin hold their first three-way summit on
  the sidelines of APEC, with Ukraine on the agenda.
- **The Hague** — the ICJ rules on the Rohingya genocide case,
  Gambia v. Myanmar.
- **Ukraine** — a third strike on the Crimean (Kerch) Bridge in a week.
- **Antalya** — COP31 climate talks go to the wire.
- **Bangladesh** — unrest spreads; the Yunus family home is torched.
- **Odisha** — Cyclone Akvan makes landfall; 100,000+ evacuated.
- **The Gulf** — Iran–Gulf clashes, and the IEA calls the Hormuz crisis
  the worst energy threat it has ever seen.
- In the ticker: Anthropic's record $81bn IPO, a record $190m Van Gogh,
  the IAEA on North Korea's uranium enrichment, and GTA VI's launch day.

## How it works

`main.ts` (Node, standard library only) copies `entry.png` into the output
directory. The program runs offline and writes the same bytes every run.

The poster itself was drawn from the day's headlines with `poster.py`
(Pillow) — a build tool that is not part of the submitted program.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
