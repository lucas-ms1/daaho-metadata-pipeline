# OCR swap Jinming check

## Methodology disclosure

- The LLM transcription model in the codebase before this run was `gpt-4o`, not `o4-mini`.
- LLM transcription was previously a fallback to Tesseract, not the primary OCR path.
- For this evaluation, LLM OCR was forced on all 19 images so the model swap affects every row.

Validation findings in new JSON outputs: 0 errors, 2 warnings.

## OCR-error rows

| Row | Status | Notes | Relevant span |
|---|---|---|---|
| BC-0692 | partial | Title: expects `Itinerary`; Transcript: expects `Nakaku`; Transcript: expects `Straits Sett`; Transcript: expects `Bombay, India:` | Upham Itinerary Address Mailing dates from Oxford, Ohio Yokohama and Japan Decembe |
| BC-0696 | no | Title: expects `William N. Jardine`; Correspondents: expects `William N. Jardine`; Transcript: expects `William N. Jardine` | October 20, 1937 President William M. Jardine University of Wichita Wichita, Kansas My dear Jardine: You may recall that when I was in your home last June I indicated with very... |
| BC-0697 | partial | Correspondents: expects `Jean Van Ausdall`; Transcript: expects `Jean Van Ausdall`; Transcript: expects `Hosack's Studio`; Transcript: expects `good condition.`; Transcript: should not contain `Dr. Heckert`; Transcript: should not contain `Red Cross`; Transcript: should not contain `Turkey tickets` | ORD Ralph McGinnis, correspondent, phone Oxford 256-J or 560-L. Miss Jean Van Ausdall, society and personals, phone Oxford 596. News items may be left at H |
| BC-0698 | partial | Title: expects `Tosses His Dime`; Transcript: should be non-empty | Tosses His Dime The Post U. S. WEATHER FORECAST: Fair, slightly warmer tonight. VO |
| BC-0703 | no | Transcript: expects `Swasdi Nitibhon` | [handwritten] Nitibhom FOREWORD Dancing, like music, is an art that has no boundaries of race and language. This little book by a native of Thailand has grown out of a voluntary... |
| BC-0708 | no | Title: expects `COLLEGE AID LETTER #4`; Transcript: expects `Sincerly` | DMINISTRATION FOR OHIO Hoster Bldg. Columbus, Ohio November 8, 1939 COLLEGE AID LETTER #4 TO: Presidents of Ohio Colleges and Universities The Washington off |
| BC-0710 | no | Location: expects `Massachusetts--Gloucester`; Transcript: expects `Wonsonhurst 59`; Transcript: expects `Gloucester, Massachusetts` | September 8, 1941 Mr. Murray Sheehan Monsomhurst 59 Gloucaster, Massachusetts Dear Murray: Replying to your letter of September 6, I can assure you that we shall be pleased to a... |
| BC-0711 | no | Transcript: expects `If he can arrange` | November 19, 1941 Mr. Murray Sheehan Royal Thai Legation 2300 Kalorama Road Washington, D. C. Dear Murray: I have just now got around to the problem of finding speakers for our... |
| BC-0713 | yes | Title: expects `26 February 1942`; Date: expects `1942-02-26`; Transcript: expects `February 26th, 1942` | S OFFICE MIAMI UNIVERSITY THE ROYAL THAI LEGATION WASHINGTON, D. C. February 26th, 1942. Mr. A.H. Upham, President of Miami University, Oxford, Ohio. My de |
| BC-0716 | partial | Transcript: expects `STUDENTS' DEPARTMENT`; Transcript: expects `[unclear]` | ROYAL THAI LEGATION STUDENTS' DEPARTMENT 2300 KALORAMA ROAD WASHINGTON, D.C. June 2, 1942 President A. H. |
| BC-0926 | no | Transcript: expects `WAR SAVINGS BONDS AND STAMPS` | [handwritten] F.13 ADDRESS OFFICIAL COMMUNICATIONS TO THE SECRETARY OF STATE WASHINGTON 25, D.C. DEPARTMENT OF STATE WASHINGTON FOR VICTORY BUY UNITED STATES WAR BONDS AND STAMP... |
| BC-0934 | partial | Transcript: expects `Provisions for vacation`; Transcript: expects `Rosa Choi`; Correspondents: expects `Ros`; Transcript: expects `18-254 Ton Am-Dong` | ks and incidental college expenses paid by Foreign Student Committee. Provisions for vacation and holiday periods -- Foreign Student Committee. STUDY OPPORTUNITY |

## Not addressed by OCR swap - flag for next round

- BC-0694, BC-0695, BC-0696, BC-0699, BC-0710, BC-0711 Creator: suspected `Upham, Alfred H.` hallucination.
- BC-0697 Title, Date, Decade, and transcript newspaper bleed: not treated as an OCR-model fix in this round.
- BC-0718 Location and handwritten transcript content: suspected hallucination.
- BC-0934 Contributors: suspected hallucinated contributors.

## Out-of-scope rows - observed change after OCR swap

| Row | Field | Observed change |
|---|---|---|
| BC-0694 | Creator | unchanged |
| BC-0695 | Creator | unchanged |
| BC-0696 | Creator | unchanged |
| BC-0699 | Creator | unchanged |
| BC-0710 | Creator | unchanged |
| BC-0711 | Creator | unchanged |
| BC-0697 | Title | unchanged |
| BC-0697 | Date | unchanged |
| BC-0697 | Decade | unchanged |
| BC-0697 | transcript newspaper bleed | now: "PAGE TWO OXFORD Ralph McGinnis, correspondent, phone Oxford 256-J or 560-L. Miss Jean Van Ausdall, society and personals, phone Oxford 596. News items may be left at Hoseck’s Studio. J. C. Byrne Drug company, business..." |
| BC-0718 | Location | unchanged |
| BC-0718 | transcript handwritten | now: "NATIONAL JAPANESE AMERICAN STUDENT RELOCATION COUNCIL 1201 Chestnut Street, Philadelphia 7, Pa. RITtenhouse 9372 John W. Nason, National Chairman C. V. Hibbard, National Director February 21, 1944 President A. H. Upha..." |
| BC-0934 | Contributors | now empty |
