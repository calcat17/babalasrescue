# Babalas Rescue+ · Summer 2026 · "Hang in there, Mzansi"

**Idea.** The climber from the logo leaves his cliff and goes on a South African summer holiday. He hangs
off the edge of Table Mountain, a rugby crossbar, the braai tongs, a Margate beach umbrella, the Uvongo
falls, festival bunting, a pool ring, the cricket stumps and a 1 January calendar page. Every piece pays
off the brand line, *we won't leave you hangin'*, and the campaign line **Hang in there, Mzansi.**
Hashtag: **#HangInThereMzansi**

## Opening in Adobe Illustrator
- **`pdf/babalas-summer-2026-all-artboards.pdf`**: open this in Illustrator. It has 30 pages and each page is a
  separate artboard at its own size (1 unit = 1 pt). It is self-contained, with images and fonts embedded.
- **`svg/*.svg`**: one editable vector file per asset, with named groups (`climber-hanging`,
  `table-mountain`, `logo-lockup`, packshots and so on). Packshots are *linked* from `brand/assets/`, so keep the
  repo folder structure, or use the PDF.
- **`png/*.png`**: full-size previews for review and posting.
- Headlines are live text set in **Futura** (Jost on screen). Install Futura PT from Adobe Fonts for
  exact type, or outline the text before sending to print.
- Rebuild: `python3 build.py`, then `node export.mjs` (needs playwright-core and Chromium; see the file header).

## The 30 assets
| # | Asset | Format / spec | File |
|---|---|---|---|
| 01 | Hero · Table Mountain · Feed 4:5 | Instagram / Facebook feed 1080×1350 | `svg/01-hero-table-mountain-feed.svg` |
| 02 | Hero · Table Mountain · Story 9:16 | Instagram / TikTok story 1080×1920 | `svg/02-hero-table-mountain-story.svg` |
| 03 | Billboard · Cape Town · 3:1 | Roadside billboard 3:1 (scale to site) | `svg/03-billboard-cape-town.svg` |
| 04 | Braai · Feed 4:5 | Instagram / Facebook feed 1080×1350 | `svg/04-braai-feed.svg` |
| 05 | Braai · Tjops Wors Rescue+ · Story | Instagram / TikTok story 1080×1920 | `svg/05-braai-story.svg` |
| 06 | Rugby · Final whistle · Feed 4:5 | Instagram / Facebook feed 1080×1350 | `svg/06-rugby-posts-feed.svg` |
| 07 | Rugby · Post-match, pre-Monday · Square | Instagram / Facebook square 1080×1080 | `svg/07-rugby-ball-square.svg` |
| 08 | Uvongo · Falls · Feed 4:5 | Instagram / Facebook feed 1080×1350 | `svg/08-uvongo-falls-feed.svg` |
| 09 | Margate · Umbrella · Feed 4:5 | Instagram / Facebook feed 1080×1350 | `svg/09-margate-umbrella-feed.svg` |
| 10 | South Coast packing list · Story | Instagram / TikTok story 1080×1920 | `svg/10-south-coast-packing-list-story.svg` |
| 11 | Breakfast run · Feed 4:5 | Instagram / Facebook feed 1080×1350 | `svg/11-breakfast-run-feed.svg` |
| 12 | Morning-after menu · Story | Instagram / TikTok story 1080×1920 | `svg/12-morning-after-menu-story.svg` |
| 13 | 1 January · Feed 4:5 | Instagram / Facebook feed 1080×1350 | `svg/13-new-years-day-feed.svg` |
| 14 | Festival season · Story | Instagram / TikTok story 1080×1920 | `svg/14-festival-season-story.svg` |
| 15 | Pool day · Square | Instagram / Facebook square 1080×1080 | `svg/15-pool-day-square.svg` |
| 16 | Beach cricket · Square | Instagram / Facebook square 1080×1080 | `svg/16-beach-cricket-square.svg` |
| 17 | Hot day, long night · Story | Instagram / TikTok story 1080×1920 | `svg/17-heat-rehydrate-story.svg` |
| 18 | Summer Survival Guide 1/5 · Carousel | Instagram carousel 1080×1080 | `svg/18-survival-guide-1-cover.svg` |
| 19 | Summer Survival Guide 2/5 · Carousel | Instagram carousel 1080×1080 | `svg/19-survival-guide-2-before-the-jol.svg` |
| 20 | Summer Survival Guide 3/5 · Carousel | Instagram carousel 1080×1080 | `svg/20-survival-guide-3-before-bed.svg` |
| 21 | Summer Survival Guide 4/5 · Carousel | Instagram carousel 1080×1080 | `svg/21-survival-guide-4-morning-after.svg` |
| 22 | Summer Survival Guide 5/5 · Carousel | Instagram carousel 1080×1080 | `svg/22-survival-guide-5-know-your-limits.svg` |
| 23 | Stock up for summer · Link ad | Facebook / Google display 1200×628 | `svg/23-link-ad-stock-up.svg` |
| 24 | In-store poster · A3 | A3 portrait poster (297×420 mm), add 3 mm bleed | `svg/24-retail-poster-a3.svg` |
| 25 | Shelf wobbler · Ø100 mm | Round shelf wobbler, die-cut on pink dashed line | `svg/25-shelf-wobbler.svg` |
| 26 | Sticker sheet · 8 die-cuts | Kiss-cut sticker sheet, die-cut on pink dashed lines | `svg/26-sticker-sheet.svg` |
| 27 | Beach towel · 70×140 cm | Beach towel 70×140 cm (print at 100 dpi full size) | `svg/27-beach-towel.svg` |
| 28 | Cooler box wrap · panel | Cooler box side panel wrap (2:1) | `svg/28-cooler-box-wrap.svg` |
| 29 | Postcard · Greetings from the morning after | Postcard A5 landscape (148×210 mm ratio) | `svg/29-postcard-greetings.svg` |
| 30 | Email header · Summer rescue plan | Email / newsletter header 1200×400 | `svg/30-email-header.svg` |

## Copy deck
| Line | Where |
|---|---|
| Hang in there, Mzansi. / Summer's long. Bounce back. | Hero (01, 02, 24) |
| Cape Town: Big nights. Bigger mornings. | Billboard (03) |
| The braai ended at 2am. The rescue starts now. | Braai (04) |
| Tjops. Wors. Rescue+ / Sunday sorted. | Braai story (05) |
| Hang on till the final whistle. / Post-match. Pre-Monday. | Rugby (06, 07) |
| Uvongo by day. Babalas by morning. | Uvongo (08) |
| Margate. Mid-December. Mid-babalas. | Margate (09) |
| South Coast packing list | Story (10) |
| Breakfast run? Bring backup. / The morning-after menu | Breakfast (11, 12) |
| New year. Same jol. Hang in there. | 1 January (13) |
| Festival season. Pack the rescue. | Festival (14) |
| Pool day. Pool night. Pool rescue. | Pool (15) |
| One hand, one bounce. Bounce back. | Beach cricket (16) |
| Hot day. Long night. Rehydrate. | Heat (17) |
| The Summer Survival Guide (before the jol, before bed, the morning after, know your limits) | Carousel (18–22) |
| Stock up for summer. / Summer survival, now in store. | Retail (23, 24) |
| Ice. Wors. Rescue+. | Cooler wrap (28) |
| Greetings from the morning after. | Postcard (29) |
| Your summer rescue plan. | Email (30) |

## Guard-rails applied
- **Responsible drinking.** Every asset carries "Please drink responsibly · 18+". The carousel ends on
  "Know your limits … never drink and drive". No copy encourages excess, and none shows driving.
- **No medical claims.** Benefit copy is limited to the ingredients the client's trade presenters list (electrolytes,
  B-vitamins, antioxidants). The "before the jol" line is the client's own copy.
- **Third-party brands.** **Wimpy** is not named or shown: using its name or logo in ads needs a co-promotion
  agreement. The breakfast pieces (11, 12) are a generic "breakfast run" and can be re-skinned if a Wimpy
  partnership is signed. **Rugby** uses generic posts and balls with no team names, emblems or team colours.
  Sports ambush-marketing rules apply to protected events. **Table Mountain, Uvongo and Margate** are used as places only,
  with no Cableway or tourism logos.
- **Palette.** Brand blue, yellow, pink and Night, plus two campaign tints (50% blue for sea, 50% yellow for sand).

## Still needed from the client
Retailer names for the "now in store" pieces, the shop URL for the email button, print specs (bleed, die-lines)
from the printer for the wobbler, stickers, towel and cooler wrap, and sign-off on the derived tints.
