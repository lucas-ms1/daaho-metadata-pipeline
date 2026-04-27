# Summary Review Notes

| Row | Classification | Notes |
|---|---|---|
| BC-0716 | confirmed-issue | The few-shot summary says Sheehan had "pleasure of having been involved in securing the commencement speaker," but the baseline transcript is conditional and regretful: "If only I could now be looking backward" and "I shall still hope in that direction!" The human CSV frames this as regret about not providing a speaker, which better matches the source. |
| BC-0698 | partially-grounded | The "broader coverage of news in Cincinnati, Ohio" phrase is grounded only as page context: the image shows *The Post*, "CINCINNATI, SATURDAY, DEC. 11, 1937," with many unrelated local/news columns. The few-shot summary does not mention key article/image details present in the source and human CSV: "avoid-the-war route," "unsettled conditions," "grounded ... about 30 miles off Formosa," "suffering from exposure," or the emergency hospital/medical attention. |
| BC-0696 | partially-grounded | The few-shot phrase "lack of publicity ... due to public perception of presidential travel" is grounded by the transcript: "I am not letting much publicity out" because "the public hardly approves of presidents doing such wasteful things." It captures the publicity concern, but the stricter "misuse of university funding" framing is not explicit in the quoted source. |
| BC-0692 | confirmed-issue | The few-shot phrase "likely related to his academic and administrative duties" is an unsupported inference. The baseline transcript contains only itinerary/address structure such as "Yokohama and Japan / December 6 - 19" and "Mailing dates / from Oxford, Ohio," while the human CSV adds purpose from external/contextual interpretation. |
| BC-0934 | confirmed-issue | The few-shot summary says "Ross Choi," while the baseline OCR says "Student Selected -- Rose Choi"; the human CSV says "Rosa Choi." The local image appears to read "Rosa Choi," so this is at least an upstream OCR/name-capture issue and should not be treated as a summary-style issue alone. |
| BC-0703 | confirmed-issue | The few-shot summary says "Swadi Nitibon," and the baseline transcript also says "Swadi Nitibon." The human CSV and local image read "Swasdi Nitibhon," so this is an OCR/name-capture issue that propagated into the summary. |

## Recommendation

Targeted re-run is recommended for BC-0716, BC-0692, BC-0934, and BC-0703 before Lucas and Alia review summaries. BC-0698 and BC-0696 can be reviewed manually, but a targeted re-run would also be reasonable if the goal is to recover omitted evidence and avoid filler.

Suggested prompt addition, not run:

> Ground every summary claim in the transcript or visible document text. Do not infer trip purpose, institutional motive, or emotional state unless the source states it directly. For names, preserve the spelling visible in the document image; if OCR and image disagree, flag uncertainty instead of choosing a new spelling. For newspaper clippings, summarize the target article and avoid page-level filler unless it materially affects the item.
