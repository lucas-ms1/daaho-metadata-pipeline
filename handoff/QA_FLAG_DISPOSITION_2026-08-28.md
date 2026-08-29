# QA Flag Disposition Ledger — August 28, 2026

This ledger adjudicates every distinct flag in
`out/ocr_swap_jinming_check_2026-05-09.md` and
`out/summary_review_notes.md`. The comparison target is the authoritative
August release. Dispositions do not authorize further record edits.

| Source note | Record | Field or span | Historical flag | Current authoritative value/state | Evidence reviewed | Disposition | Rationale | Successor action |
|---|---|---|---|---|---|---|---|---|
| OCR swap | BC-0692 | title | Expected “Itinerary” | `Upham itinerary document, undated` | August JSON; image | false positive | The canonical sentence-case title includes the asserted concept. | None. |
| OCR swap | BC-0692 | transcript: `Nakaku` | OCR had `Nakku` | Still `Nakku` | August JSON/raw; image visibly reads `Nakaku` | deferred successor work | Real one-letter OCR error, but it was not among the five authorized corrections. | Seek authority before a versioned transcript correction. |
| OCR swap | BC-0692 | transcript: Straits Settlements | Expected `Straits Sett...` | `Singapore, Straits Settlements` | August JSON/raw; image | false positive | The authoritative transcript already contains the full wording. | None. |
| OCR swap | BC-0692 | transcript: Bombay address | Expected `Bombay, India` | `Bombay, India` | August JSON/raw; image | false positive | The expected address is present. | None. |
| Summary review | BC-0692 | description claim | Few-shot inferred academic/administrative trip purpose | Current description only describes itinerary destinations/addresses | August JSON; historical few-shot note | false positive | False positive as a blocker to the authoritative August release; the unsupported inference applies to discarded few-shot output. | Revisit summary style only in a new authorized project. |
| OCR swap | BC-0694 | creator | Suspected hallucinated `Upham, Alfred H.` on unsigned “President” letter | Creator remains `Upham, Alfred H.` | August JSON/raw; image ends only `President` | deferred successor work | Attribution is plausible from collection context but is a creator-policy judgment, not image-explicit. | Advisor should define policy for unsigned office-authored letters. |
| OCR swap | BC-0695 | creator | Suspected hallucinated `Upham, Alfred H.` on unsigned “President” letter | Creator remains `Upham, Alfred H.` | August JSON/raw; image ends only `President` | deferred successor work | Same unresolved creator-policy question. | Advisor policy decision. |
| OCR swap | BC-0696 | title/name | Expected William N. Jardine; current said M. | Title still says William M. Jardine | August JSON/raw; image visibly reads William N. Jardine | deferred successor work | The historical expectation is correct, but this record was not authorized for August correction. | Correct title in a future authorized release. |
| OCR swap | BC-0696 | correspondents/name | Expected William N. Jardine | Correspondent remains William M. Jardine | August JSON/raw; image | deferred successor work | Real name error outside approved five. | Correct with title/transcript under explicit authority. |
| OCR swap | BC-0696 | transcript/name | Expected William N. Jardine | Transcript remains William M. Jardine | August JSON/raw; image | deferred successor work | Real OCR error outside approved five. | Correct as a synchronized future change. |
| OCR swap | BC-0696 | creator | Suspected hallucinated `Upham, Alfred H.` | Creator remains `Upham, Alfred H.` | August JSON/raw; image ends only `President` | deferred successor work | Creator attribution depends on collection/office policy. | Advisor policy decision. |
| Summary review | BC-0696 | description claim | Few-shot overstated “misuse of university funding” | Current description states sabbatical travel plans | August JSON; image; historical note | false positive | False positive as a blocker to the authoritative August release; the criticized phrasing belongs to discarded few-shot output. | None unless summaries are re-scoped. |
| OCR swap | BC-0697 | correspondents: Jean Van Ausdall | OCR/name mismatch | `Miss Jeni Van Ausdal` | August JSON/raw; image visibly reads Jean Van Ausdall | deferred successor work | Real name OCR error outside approved five. | Correct correspondent and transcript together if authorized. |
| OCR swap | BC-0697 | transcript: Jean Van Ausdall | OCR/name mismatch | `Miss Jeni Van Ausdal` | August JSON/raw; image | deferred successor work | Real OCR error. | Same as above. |
| OCR swap | BC-0697 | transcript: Hosack's Studio | OCR had `Honack's Studio` | Still `Honack's Studio` | August JSON/raw; image visibly reads Hosack's | deferred successor work | Real OCR error outside approved five. | Future authorized transcript correction. |
| OCR swap | BC-0697 | transcript: `good condition` | Expected phrase | Phrase is present | August JSON/raw; image | false positive | The phrase is already captured, although it belongs to an unrelated neighboring advertisement. | Do not treat it as target-item metadata. |
| OCR swap | BC-0697 | transcript: Dr. Heckert | Should not contain unrelated column | Present | August JSON/raw; image | accepted limitation | Full-page OCR includes adjacent newspaper-column bleed beyond the target article. | Crop/retranscribe only in a future versioned OCR project. |
| OCR swap | BC-0697 | transcript: Red Cross | Should not contain unrelated column | Present | August JSON/raw; image | accepted limitation | Same neighboring-column bleed. | Same as above. |
| OCR swap | BC-0697 | transcript: Turkey tickets | Should not contain unrelated column | Present | August JSON/raw; image | accepted limitation | Same neighboring-column bleed. | Same as above. |
| OCR swap | BC-0697 | title | Flagged as non-OCR issue | `Dr. Upham and family planning trip to Japan, 16 November 1937` | August JSON; image headline | false positive | Title accurately represents the target article. | None. |
| OCR swap | BC-0697 | date | Flagged as non-OCR issue | `1937-11-16` | August JSON; image dateline | false positive | The visible dateline is Oxford, Nov. 16, and the page context is 1937. | None. |
| OCR swap | BC-0697 | decade | Flagged as non-OCR issue | `1930-1939` | August JSON; date-derived value | false positive | Decade is deterministically consistent with the valid date. | None. |
| OCR swap | BC-0697 | transcript scope | General newspaper bleed | Target article plus neighboring text | August JSON/raw; full image | accepted limitation | Item metadata is valid, but transcript scope is broader than the target article. | Consider crop-based OCR later; do not reopen August release. |
| OCR swap | BC-0698 | title capitalization | Expected `Tosses His Dime` | `Tosses his dime, 11 December 1937` | August JSON; image | false positive | Canonical title is intentionally sentence-cased and date-suffixed. | None. |
| OCR swap | BC-0698 | transcript | Blank transcript | Manual target-article transcript is nonblank | August JSON; image; correction log | corrected in the August release | Authorized recovery includes the Miami rescue article and related caption only. | None. |
| Summary review | BC-0698 | description scope | Few-shot summary used page-context filler and omitted article details | Current description identifies the rescue article | August JSON; image; correction log | false positive | False positive as a blocker to the authoritative August release; the detailed criticism applies to discarded few-shot output. | Broader summary enrichment only if reauthorized. |
| OCR swap | BC-0699 | creator | Suspected hallucinated `Upham, Alfred H.` on unsigned “President” letter | Creator remains `Upham, Alfred H.` | August JSON/raw; image ends only `President` | deferred successor work | Creator-policy judgment remains unresolved. | Advisor policy decision. |
| OCR swap | BC-0703 | transcript/name | Expected Swasdi Nitibhon | Transcript now says Swasdi Nitibhon | August JSON; image; correction log | corrected in the August release | Human-approved spelling synchronized in transcript. | None. |
| Summary review | BC-0703 | description/name | Few-shot propagated `Swadi Nitibon` | Description now says Swasdi Nitibhon | August JSON; image; correction log | corrected in the August release | Authoritative description no longer contains the experimental misspelling. | None. |
| Correction log (related review) | BC-0703 | contributors | Whether Nitibhon should be added | Contributors remain null with human-review provenance | August JSON; correction log | corrected in the August release | The approved decision is not to add him because the foreword discusses him but is neither written by nor addressed to him. | None unless policy changes. |
| OCR swap | BC-0708 | title | Expected all-caps `COLLEGE AID LETTER #4` | `College aid letter #4, 8 November 1939` | August JSON; image | false positive | Canonical title normalization is intentional and content-preserving. | None. |
| OCR swap | BC-0708 | transcript closing | Expected source typo `Sincerly` | Transcript normalizes to `Sincerely` | August JSON/raw; image reads `Sincerly` | accepted limitation | Minor source-faithfulness normalization outside approved corrections. | Preserve literal spelling only in a future authorized transcript edition. |
| OCR swap | BC-0710 | place | Expected controlled `Massachusetts--Gloucester` | Exactly that value | August JSON; correction log; validation report | corrected in the August release | Human-approved controlled-vocabulary correction. | Retain the accepted evidence warning. |
| OCR swap | BC-0710 | transcript address line | Expected `Wonsonhurst 59` | `Monsonhurst 59` | August JSON/raw; image visibly reads Monsonhurst | false positive | The old expectation was wrong. | None. |
| OCR swap | BC-0710 | transcript source place | Expected normalized `Gloucester, Massachusetts` | Source-faithful `Glouchester, Massachusetts` | August JSON/raw; image; correction log | accepted limitation | Controlled metadata is corrected while literal source spelling is intentionally retained; this produces the single accepted warning. | Advisor acknowledgment; do not normalize transcript silently. |
| OCR swap | BC-0710 | creator | Suspected hallucinated `Upham, Alfred H.` | Creator remains `Upham, Alfred H.` | August JSON/raw; image ends only `President` | deferred successor work | Unresolved creator-policy judgment. | Advisor policy decision. |
| OCR swap | BC-0711 | transcript clause | Expected `If he can arrange` | `If he will arrange` | August JSON/raw; image visibly reads `If he can arrange` | accepted limitation | Minor OCR substitution outside approved five. | Future authorized transcript correction if desired. |
| OCR swap | BC-0711 | creator | Suspected hallucinated `Upham, Alfred H.` | Creator remains `Upham, Alfred H.` | August JSON/raw; image ends only `President` | deferred successor work | Unresolved creator-policy judgment. | Advisor policy decision. |
| OCR swap | BC-0713 | title | Expected 26 February 1942 | Title uses 26 February 1942 | August JSON; image; correction log | corrected in the August release | Human-approved synchronized correction. | None. |
| OCR swap | BC-0713 | date | Expected `1942-02-26` | Exactly that date | August JSON; image; correction log | corrected in the August release | Human-approved synchronized correction. | None. |
| OCR swap | BC-0713 | transcript date | Expected `February 26th, 1942` | Exactly that text | August JSON; image; correction log | corrected in the August release | Human-approved synchronized correction. | None. |
| OCR swap | BC-0716 | transcript letterhead | Expected `STUDENTS' DEPARTMENT` | `STUDENT'S DEPARTMENT` | August JSON/raw; image visibly uses plural possessive | deferred successor work | Real minor OCR error outside approved five. | Future authorized transcript correction. |
| OCR swap | BC-0716 | handwritten signature | Expected `[unclear]` marker | Signature ends `Murry [unclear]` | August JSON/raw; image | false positive | The uncertainty marker is already present. | None. |
| Summary review | BC-0716 | description claim | Few-shot incorrectly claimed speaker was secured | Current description expresses appreciation and admiration, not that claim | August JSON; image; historical note | false positive | False positive as a blocker to the authoritative August release; applies to discarded few-shot output. | None unless summaries are re-scoped. |
| OCR swap | BC-0718 | place | Suspected hallucination | `Pennsylvania--Philadelphia; Ohio--Oxford` | August JSON/raw; image shows Philadelphia sender and Oxford recipient | false positive | Both controlled places are visibly grounded. | None. |
| OCR swap | BC-0718 | handwritten/signature content | Suspected hallucination | C. V. Hibbard letter and signature are represented | August JSON/raw; image | false positive | The visible letterhead, body, and signature support the authoritative state. | None. |
| OCR swap | BC-0926 | transcript emblem text | Expected `WAR SAVINGS BONDS AND STAMPS` | Phrase is present in authoritative transcript | August JSON/raw; image | false positive | The old blocker is already satisfied in the authoritative record. | None. |
| OCR swap | BC-0934 | transcript: provisions | Expected plural `Provisions for vacation` | Singular `Provision for vacation` | August JSON/raw; image visibly reads plural | accepted limitation | Minor OCR number mismatch not included in the approved corrections. | Correct only in a future authorized version. |
| OCR swap / Summary review | BC-0934 | transcript: Rosa Choi | Expected Rosa rather than Rose/Ross | `Rosa Choi` | August JSON; image; correction log | corrected in the August release | Human-approved name correction. | None. |
| OCR swap | BC-0934 | correspondents | Historical OCR had truncated/wrong `Ros...` | `Rosa Choi` | August JSON; correction log | corrected in the August release | Human approved correspondent membership and spelling. | None. |
| OCR swap | BC-0934 | transcript address | Expected `18-254 Ton Am-Dong` | Exactly that address | August JSON; image; correction log | corrected in the August release | Human-approved address correction. | None. |
| OCR swap | BC-0934 | contributors | Suspected hallucinated contributors | Carol L. Anderson, Paul F. Erwin, Ernest H. Hahne | August JSON; visible signatures; correction log | corrected in the August release | Signatories are visibly grounded; Hahne spelling was corrected. | None. |
| Summary review | BC-0934 | description/name claim | Few-shot used Ross Choi | Authoritative description does not repeat the wrong name; authoritative name fields use Rosa | August JSON; image; correction log | corrected in the August release | The upstream name issue and authoritative representation are corrected; the few-shot output is discarded. | None. |

## Totals

| Disposition | Count |
|---|---:|
| corrected in the August release | 13 |
| false positive | 18 |
| accepted limitation | 8 |
| deferred successor work | 14 |
| **Total distinct issues/claims** | **53** |

## Deferred successor work

- `BC-0692`: correct `Nakku` to source-visible `Nakaku` if authorized.
- `BC-0696`: synchronize William N. Jardine across title, correspondent, and transcript.
- `BC-0697`: correct Jean Van Ausdall and Hosack's Studio; separately decide whether to crop/retranscribe the target article.
- `BC-0716`: correct the letterhead to `STUDENTS' DEPARTMENT` if authorized.
- Establish a creator-attribution policy for the unsigned “President” letters in
  `BC-0694`, `BC-0695`, `BC-0696`, `BC-0699`, `BC-0710`, and `BC-0711`.

Deferred flags were documented rather than used to reopen or silently modify the approved August release.

## Advisor acknowledgment requested

Please acknowledge the accepted limitations (minor source-faithfulness/OCR
variants, `BC-0697` newspaper bleed, and the intentional `BC-0710` warning) and
decide whether the deferred OCR/name and unsigned-letter creator-policy items
belong in a successor release. No acknowledgment is claimed in this repository.
