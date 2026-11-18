# The World in One Page — 18 November 2026

Entry for the make.fun bounty **"Sum up 18 November's world news in one image"**
(`news-image-20261118`).

A newspaper front page rendered programmatically with Python + PIL
(`render_image.py`, no network, no AI generation): the US–Iran tit-for-tat
in the Strait of Hormuz leads, with Ukraine's second-day strike on the
Crimea bridge, Trump's Quad talks in Manila, the UN's warning of cold
deaths in Gaza, and the COP31 draft deal in Antalya — plus the An-12 crash
in Siberia and Nvidia's Q3 earnings in the ALSO strip.

Layout is a broadsheet-style grid, not stacked rows: full-width lead
headline with a large lead photo, a two-column middle row (Ukraine with
photo, Diplomacy text-only with a Thursday box), and a bottom row of two
horizontal strips (Gaza, COP31).

## Photos

All photos are real photographs, freely licensed, each verified against
its source page. Files live in `photos/`.

| File | Depicts | Source | Licence |
| ---- | ------- | ------ | ------- |
| `lead_carrier.jpg` | US Navy ships sail in formation during RIMPAC 2026 (USS Essex in front) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:260722-N-BR246-2100_USS_Theodore_Roosevelt_leads_group_sail_during_RIMPAC_2026.jpg) — U.S. Navy photo by Mass Communication Specialist 3rd Class Aaron Haro Gonzalez | Public domain |
| `bridge_collapse.jpg` | The Crimean Bridge after the 16–17 November 2026 strikes | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:KerchBridgeCollapse.jpg) — Security Service of Ukraine, via ssu.gov.ua, 17 Nov 2026 | CC BY 4.0 |
| `cop31.jpg` | COP31 President of Negotiation Chris Bowen (left) and EU Commissioner Dan Jørgensen, Antalya, 10 Nov 2026 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Chris_Bowen,_COP31_President_of_Negotiation_%26_Dan_J%C3%B8rgensen,_European_Commissioner.jpg) — Necati Savas / European Union 2026 / EC Audiovisual Service | CC BY 4.0 |
| `gaza_tents.jpg` | Flooded tents of displaced Palestinians, Deir el-Balah, Gaza Strip, Jan 2025 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Flooded_tents_of_displaced_Palestinians_due_to_heavy_rain_in_Deir_el-Balah,_Gaza_Strip.jpg) — UNRWA photo by Ashraf Amra | CC BY-SA 3.0 IGO |

Notes:

- No freely licensed photo of the actual burning tanker Tara Gas exists:
  the fire was only captured in social-media video and news-agency
  footage, which is not freely licensed. The lead photo therefore shows
  the US naval presence (a third US carrier arrived in the region) rather
  than the fire itself.
- The Diplomacy story is text-only: no freely licensed photo of the
  17 November Manila Quad meeting was available when this was built (the
  group photo is AP-copyrighted; no White House photo had reached
  Wikimedia Commons yet).
- The ALSO strip is text-only by design.

## Run

```sh
python3 render_image.py   # writes entry.png (1024x1024, <= 1 MiB)
python3 main.py           # copies entry.png to /output/entry.png
```

`main.py` is the entrypoint: it only copies the finished image, so two runs
write byte-identical output.

## License

MIT — see `LICENSE`.
