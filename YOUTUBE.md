# YouTube text: titles and description

Every video gets `videos/<slug>/youtube.md` (scaffolded from `template/youtube.md`): **three titles** to choose from and the
**description**, ready to paste. Write it in PIPELINE step 9, together with the three thumbnails.

## Titles
- Three, each paired with one thumbnail (`thumbnails/<name>_thumbnail_1..3.png`, same order) and the same concept
  (THUMBNAIL.md "Three thumbnails": the hook question, the surprise, the stakes or open question).
- Under ~60 characters so YouTube does not cut them; plain words a non-expert would search for; honest (no promise the
  video does not keep, no "proof" for an open problem). Model: "How Hashing Works: Inside SHA-512".

## Description: five parts, in this order
1. **The video**: 2–3 short paragraphs. Open with the video's own hook image, say what the viewer will see and come away
   understanding, and one honesty line (what was computed, what is still open). No hype words.
2. **Chapters** under `CHAPTERS`: `cd src && python3 tools/chapters.py` gives the start of every scene from the frozen
   timeline; keep the times, rewrite the titles for viewers. First chapter 0:00 (YouTube needs it).
3. **About AERTHEON** under `ABOUT AERTHEON`: exactly this paragraph, the same in every video:

   > AERTHEON makes educational videos on mathematics, computer science and engineering. Every idea is built up from simple examples and explained step by step, so anyone can follow along, no background needed.

4. **Sources** under `SOURCES`: one per line, `Short label: https://…`. Plain URLs (YouTube turns them into links; Markdown
   link syntax does not work there). Take them from `src/script/research_facts.md`; prefer primary sources (standards,
   papers, official announcements) for every claim, date and number the video states; Wikipedia only for background.
   Check each one loads: `curl -s -o /dev/null -L -w '%{http_code}' -A 'Mozilla/5.0' <url>` must print 200.
5. **Hashtags** at the very bottom: 5–8, topic first, then field (`#Mathematics`, `#ComputerScience`, `#Engineering`),
   then `#Explained`. YouTube shows the first three above the title.

The description goes inside the ```text block of `youtube.md` as plain text (no Markdown inside it), so the user can copy
it in one piece. Done when: no `{{…}}` placeholder is left and every source URL returned 200.
