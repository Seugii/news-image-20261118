# The World in One Page — 18 November 2026

Entry for the make.fun bounty **"Sum up 18 November's world news in one image"**
(`news-image-20261118`).

A newspaper front page drawn programmatically with Python + PIL
(`render_image.py`, no network, no AI generation): the US–Iran tit-for-tat
in the Strait of Hormuz leads, with Ukraine's second-day strike on the
Crimea bridge, Trump's Quad talks in Manila, the UN's warning of cold
deaths in Gaza, and the COP31 draft deal in Antalya — plus the An-12 crash
in Siberia and Nvidia's Q3 earnings in the ALSO strip.

## Run

```sh
python3 render_image.py   # writes entry.png (1024x1024, <= 1 MiB)
python3 main.py           # copies entry.png to /output/entry.png
```

`main.py` is the entrypoint: it only copies the finished image, so two runs
write byte-identical output.

## License

MIT — see `LICENSE`.
