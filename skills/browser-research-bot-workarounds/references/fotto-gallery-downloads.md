# Fotto / Gabby gallery downloads

Session note: Gabby Produções gallery pages are Next.js and embed the media catalog in SSR JSON (`self.__next_f.push(...)`) inside the HTML.

What was available on page 14:
- `thumbnail`: public thumbnail URL under `https://images.fotto.com.br/store/<store>/thumb/...`
- `image`: public preview URL under `https://images.fotto.com.br/store/<store>/preview/...`
- `width` / `height` fields in the JSON matched the preview image dimensions

Observed sizes on one sample:
- thumbnail: `200x300`
- preview: `533x800`

Takeaways:
- Browser DOM inspection only showed thumbnail `<img>` elements.
- The better source was the HTML payload, not the rendered page.
- Regex extraction from the SSR JSON was enough to collect all preview URLs for the page.
- The full-resolution/original files were not exposed publicly in the HTML; they appear to live behind the modal / purchase flow.

Useful extraction pattern:
- Fetch page HTML with `requests`.
- Regex for preview URLs:
  `https://images\.fotto\.com\.br/store/[^\"\\]+/preview/[^\"\\]+`
- Deduplicate the results and download in parallel.
