# OCR swap CSV diff

## Methodology disclosure

- The LLM transcription model in the codebase before this run was `gpt-4o`, not `o4-mini`.
- LLM transcription was previously a fallback to Tesseract, not the primary OCR path.
- For this evaluation, LLM OCR was forced on all 19 images so the model swap affects every row.

Old CSV: `out/final_metadata_2026-04-27_handoff.csv`
New CSV: `out/final_metadata_2026-05-09_ocr-gpt54mini.csv`

### BC-0688
- Title: "Letter to Miss Marshall from Murray Sheehan, 27 October 1938" -> "Letter regarding Mr. Prasobsukh Sukhsvasti, 27 October 1938"
- Correspondents: "Miss Marshall" -> "Marshall, Miss; Rosser, Aurelia; Sukhsvasti, Prasobsukh"
- Summary: "A letter from Murray Sheehan of the Siamese Legation to the secretary to the president of Miami University regarding the listing of Mr. Prasobsukh Sukhsvasti and the request to not grant him the title 'Prince'." -> "A letter from Murray Sheehan, Superintendent of the Siamese Legation, to Miss Marshall, Secretary to the President of Miami University, dated 27 October 1938. The letter provides the address and occupation of Mr. Pras..."
- Subject (FAST): "Miami University (Oxford, Ohio)" -> "correspondence; Miami University (Oxford, Ohio); international students"
- Genre: "correspondence" -> "letters (correspondence)"
- transcript: "STUDENTS' DEPARTMENT" -> "[handwritten] 1 RP [handwritten] 2 [handwritten] Mn Mr's - Pls note return [handwritten] e?ty STUDENTS' DEPARTMENT"
- transcript: "2300 KALORAMA ROAD" -> "2300 KALORAMA ROAD"
- transcript: "Secretary to the President Miami University" -> "Secretary to the President Miami University"
- transcript: "Miss Aurelia Rosser has written to say that you would like to have Mr. Prasobsukh Sukhsvasti's present address and occupation for the 1938 graduate files." -> "Miss Aurelia Rosser has written to say that you would like to have Mr. Prasobsukh Sukhsvasti's present address and occupation for the 1938 graduate files."
- transcript: "Mr. Sukhsvasti should be listed as M. C. Prasobsukh Sukhsvasti, 10 Pra Aditya Road, Bangkok, Siam. I should like again, as on previous occasions, to request that the title of \"Prince\" be not granted to him by Miami Un..." -> "Mr. Sukhsvasti should be listed as M. C. Prasobsukh Sukhsvasti, 10 Pra Aditya Road, Bangkok, Siam. I should like again, as on previous occasions, to request that the title of \"Prince\" be not granted to him by Miami Un..."

### BC-0692
- Summary: "Document detailing the travel itinerary for Upham, listing destinations and addresses of American Express branches from December to March." -> "This document outlines the travel itinerary of Alfred H. Upham, president of Miami University (1928-1945), detailing mailing dates and locations from Oxford, Ohio. The itinerary includes stops in Yokohama, Manila, Sin..."
- Subject (FAST): "correspondence" -> "travel"
- transcript: "" -> "Address Mailing dates from Oxford, Ohio"
- transcript: "" -> "American Express Co. 7 Nihon Odori, Nakaku (P. O. Box 407) Yokohama, Japan November 17 - 24"
- transcript: "Singapore January 9 - 27 Calcutta February 6 - 7 Bombay February 17 - 18 Cairo February 28 - March 14 Naples and Italy March 19 - April 10 Address American Express Co. 7 Nihon Odori, Nakku (P. O. Box 407) Yokohama, Japan" -> ""
- transcript: "" -> "November 24 - December 1 Singapore January 9 - 27"
- transcript: "Singapore, Straits Settlements" -> "Singapore, Straits Sett*ments December 1 - 14 Calcutta February 6 - 7"

### BC-0694
- Title: "Letter to Mr. Kiyoshi Tomizawa from the President, 19 October 1937" -> "Letter to Mr. Kiyoshi Tomizawa from Alfred H. Upham, 19 October 1937"
- Correspondents: "Mr. Kiyoshi Tomizawa" -> "Tomizawa, Kiyoshi"
- Location: "California--San Francisco; Ohio--Oxford" -> "California--San Francisco"
- Summary: "A letter from Alfred H. Upham, president of Miami University (1928–1945), to Mr. Kiyoshi Tomizawa, discussing a planned winter vacation around the world by the Upham family and a potential meeting in San Francisco." -> "A letter from Alfred H. Upham, president of Miami University (1928-1945), to Mr. Kiyoshi Tomizawa, dated October 19, 1937. Upham discusses his family's plans for a winter vacation involving a trip around the world, wi..."
- Subject (FAST): "Vacations--Planning; World War (1939-1945); correspondence" -> "correspondence; Miami University (Oxford, Ohio); travel"
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "1826 Bush Street" -> "1528 Bush Street"
- transcript: "All summer and fall the Upham family have been planning a winter vacation which would take the shape of a trip around the world. In spite of many discouragements we are still hopeful of carrying out our plans. If we d..." -> "All summer and fall the Upham family have been planning a winter vacation which would take the shape of a trip around the world. In spite of many discourage- ments we are still hopeful of carrying out our plans. If we..."
- transcript: "We all enjoyed your visit to Oxford in June quite as much as I suspect you did. You reestablished many warm friendships here, and we are all proud of the work you are doing." -> "We all enjoyed your visit to Oxford in June quite as much as I suspect you did. You reestablished many warm friendships here, and we are all proud of the work you are doing."

### BC-0695
- Title: "Letter to His Excellency, the Minister from Siam, 20 October 1937" -> "Letter to the Minister from Siam regarding Prasob Sukhvashti, 20 October 1937"
- Correspondents: "His Excellency, the Minister from Siam; Prasob Sukhvashti" -> ""
- Summary: "A letter from Alfred H. Upham, president of Miami University (1928–1945), to the Minister from Siam, discussing the achievements and future plans of Prasob Sukhvashti, who is returning to complete his studies." -> "A letter from Alfred H. Upham, president of Miami University (1928-1945), to the Minister from Siam at the Siamese Legation in Washington, D.C. The letter discusses Prasob Sukhvashti, a student who returned to Miami U..."
- Subject (FAST): "education; international students" -> "correspondence; Miami University (Oxford, Ohio); international students"
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "Prasob Sukhvashti, who has returned to Miami University this fall to continue his college course here, has asked me to write you regarding the record and impression he has made on our campus." -> "Prasob Sukhvashti, who has returned to Miami University this fall to continue his college course here, has asked me to write you regarding the record and impression he has made on our campus."
- transcript: "During his earlier residence with us we all came to think very highly of him, both on account of his natural ability and because of the determination with which he went to work to improve upon his record in the east a..." -> "During his earlier residence with us we all came to think very highly of him, both on account of his natural ability and because of the determination with which he went to work to improve upon his record in the east a..."
- transcript: "There is every indication that the young man has entered upon his work this fall with the same fine spirit he manifested before. In the interval he has had added experience in teaching and in newspaper work, so that h..." -> "There is every indication that the young man has entered upon his work this fall with the same fine spirit he manifested before. In the interval he has had added ex- perience in teaching and in newspaper work, so that..."

### BC-0696
- Title: "Letter to President William M. Jardine, 20 October 1937" -> "Letter to President William M. Jardine from Alfred H. Upham, 20 October 1937"
- Correspondents: "President William M. Jardine" -> "Jardine, William M."
- Location: "Kansas--Wichita" -> "Ohio--Oxford; Kansas--Wichita"
- Summary: "A letter from Alfred H. Upham, president of Miami University (1928–1945), to President William M. Jardine of the University of Wichita, discussing plans for a sabbatical trip around the world, including stops in Cairo..." -> "A letter from Alfred H. Upham, president of Miami University (1928-1945), to President William M. Jardine of the University of Wichita. Upham discusses his plans for a sabbatical leave involving a trip around the worl..."
- Subject (FAST): "university presidents; Vacations--Planning; correspondence" -> "correspondence; Miami University (Oxford, Ohio); travel"
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "President William M. Jardine University of Wichita Wichita, Kansas" -> "President William M. Jardine University of Wichita Wichita, Kansas"
- transcript: "My dear Jardine:" -> "My dear Jardine:"
- transcript: "You may recall that when I was in your home last June I indicated with very little confidence that the Uphams were hoping to utilize a sabbatical leave for winter vacation this year for a trip around the world. One ob..." -> "You may recall that when I was in your home last June I indicated with very little confidence that the Uphams were hoping to utilize a sabbatical leave for winter vacation this year for a trip around the world. One ob..."
- transcript: "I am wondering if in the light of your experience and acquaintance there you would have any suggestions you would care to offer or would indicate any people whom we ought to see. I am told that this is the busiest tim..." -> "I am wondering if in the light of your experience and acquaintance there you would have any suggestions you would care to offer or would indicate any people whom we ought to see. I am told that this is the busiest tim..."
- transcript: "I am not letting much publicity out in regard to this winter trip, because however valuable it may be for professors to enjoy sabbatical travel, the public hardly approves of presidents doing such wasteful things." -> "I am not letting much publicity out in regard to this winter trip, because however valuable it may be for professors to enjoy sabbatical travel, the public hardly approves of presidents doing such wasteful things."

### BC-0697
- Correspondents: "Ralph McGinnis; Miss Jeni Van Ausdal" -> ""
- Summary: "A newspaper clipping from the Journal-News detailing Dr. Alfred H. Upham's planned trip to Japan for a sabbatical to study educational methods and visit Miami University alumni. The Upham family will visit several cou..." -> "This newspaper clipping from the Journal-News, dated 16 November 1937, details the travel plans of Dr. A. H. Upham, president of Miami University, along with his family. They are set to leave San Francisco for a sabba..."
- Subject (FAST): "American students; foreign students; Miami University (Oxford, Ohio)" -> "correspondence; Miami University (Oxford, Ohio); travel; education"
- transcript: "Miss Jeni Van Ausdal, society and personals, phone Oxford 596. News items may be left at Honack's Studio." -> "Miss Jean Van Ausdall, society and personals, phone Oxford 596. News items may be left at Hoseck’s Studio."
- transcript: "Oxford, Nov. 16. Dr. A. H. Upham, Miami president, Mrs. Upham, and daughter, Peggy, will leave this week for a winter vacation which will be in the nature of a Sabbatical leave. The Uphams plan to leave San Francisco..." -> "Oxford, Nov. 16. Dr. A. H. Upham, Miami president, Mrs. Upham, and daughter, Peggy, will leave this week for a winter vacation which will be in the nature of a Sabbatical leave. The Uphams plan to leave San Francisco..."
- transcript: "FOR SALE—Electric stove in good condition, Apply McGreevy Dairy and Ice Co., Dixie highway. 79-2t" -> "FOR SALE—Electric stove in good condition. Apply McGreevy Dairy and Ice Co., Dixie highway. 79—2t"
- transcript: "the American Association for the Advancement of Science to give the guest address at their December meeting in Indianapolis. During the speech, Dr. Evans will show 24 reels of motion pictures which he took last summer..." -> "the American Association for the Advancement of Science to give the guest address at their December meeting in Indianapolis. During the speech, Dr. Evans will show 24 reels of motion pictures which he took last summer..."
- transcript: "The Red Cross roll-call in Oxford will be conducted by students of Stewart and McGuffey schools. Dr. J. W. Heckert will serve as chairman of the canvass which will be held November 18, 19, and 20 through November 30." -> ""

### BC-0698
- Title: "Tosses his dime, 11 December 1937" -> "Miami U. president among 503 rescued from grounded liner, 11 December 1937"
- Summary: "A newspaper article from The Post discussing the rescue of Alfred H. Upham, president of Miami University, among 503 passengers from a grounded liner." -> "A newspaper clipping from The Post, dated 11 December 1937, reporting on the rescue of Miami University President Alfred H. Upham among 503 passengers from a grounded liner. The article also covers the Japanese milita..."
- Subject (FAST): "correspondence" -> "Miami University (Oxford, Ohio); correspondence; Japanese Americans; World War (1939-1945)"
- transcript: "" -> "Tosses His Dime The Post U. S. WEATHER FORECAST: Fair, slightly warmer tonight. VOL. 114. NO. 141. CINCINNATI, SATURDAY, DEC. 11, 1937. Entered at Cincinnati as Second Class Matter Jan. 15, 1881. Act of 1879. HAMILTON..."

### BC-0699
- Title: "Letter to Mr. Koichi Hasegawa, 19 October 1937" -> "Letter to Mr. Koichi Hasegawa from the president, 19 October 1937"
- Correspondents: "Mr. Koichi Hasegawa" -> "Hasegawa, Koichi"
- Location: "" -> "Ohio--Oxford; Japan--Osaka"
- Summary: "A letter from Alfred H. Upham, president of Miami University (1928–1945), to Mr. Koichi Hasegawa in Osaka, detailing winter travel plans in Japan during 1937 despite difficulties." -> "A letter from Alfred H. Upham, president of Miami University (1928-1945), to Mr. Koichi Hasegawa in Osaka, Japan, dated 19 October 1937. Upham discusses his family's planned winter vacation, which includes a trip arou..."
- Subject (FAST): "Vacations--Planning; travel" -> "correspondence; Miami University (Oxford, Ohio)"
- transcript: "Mr. Koichi Hasegawa 57 Naka 1 Chome Sonezaki, Kitaku Osaka, Japan" -> "Mr. Koichi Hasegawa 57 Naka 1 Chome Sonezaki, Kitaku Osaka, Japan"
- transcript: "My dear Hasegawa:" -> "My dear Hasegawa:"
- transcript: "In spite of many discouragements the Upham family is still planning quite definitely a winter vacation which will take the form of a trip around the world. We shall have to be detoured around China, but we still have..." -> "In spite of many discouragements the Upham family is still planning quite definitely a winter vacation which will take the form of a trip around the world. We shall have to be detoured around China, but we still have..."
- transcript: "Our present plan is to reach Yokohama on the President Hoover on the morning of Saturday, November 27. We have reservations at the Imperial Hotel in Tokyo for several days. We are to reach Kioto Wednesday afternoon, D..." -> "Our present plan is to reach Yokohama on the President Hoover on the morning of Saturday, November 27. We have reservations at the Imperial Hotel in Tokyo for several days. We are to reach Kioto Wednesday afternoon, D..."
- transcript: "With all good wishes," -> "With all good wishes,"

### BC-0703
- Creator: "Upham, A. H." -> "Upham, Alfred H."
- Summary: "A foreword written by A. H. Upham, discussing a ballroom dancing class led by Swadi Nitibon from Thailand at Miami University." -> "This foreword by Alfred H. Upham, president of Miami University (1928-1945), introduces a book by Swasdi Nitibhom, a native of Thailand. The book is based on a ballroom dancing class conducted by Nitibhom for American..."
- Subject (FAST): "dancing; cultural exchange; Thailand; American students" -> "Miami University (Oxford, Ohio); international students; Thailand"
- Language: "English" -> ""
- transcript: "Dancing, like music, is an art that has no boundaries of race and language. This little book by a native of Thailand has grown out of a voluntary class in ball-room dancing conducted by him for a typical group of Amer..." -> "[handwritten] Nitibhom"
- transcript: "Swadi Nitibon and the little group of other young men from Thailand who have chosen to live and work for a time among us are very welcome here at Miami University. They have sent our imaginations questing half way aro..." -> "FOREWORD Dancing, like music, is an art that has no boundaries of race and language. This little book by a native of Thailand has grown out of a voluntary class in ball-room dancing con- ducted by him for a typical gr..."

### BC-0708
- Contributors: "Harry E. Rabe" -> ""
- Correspondents: "Presidents of Ohio Colleges and Universities" -> ""
- Summary: "A letter from the National Youth Administration for Ohio requesting information from Ohio Colleges and Universities regarding participation in the NYA College and Graduate Aid Program." -> "A letter dated November 8, 1939, from S. Burns Weston, State Administrator of the National Youth Administration for Ohio, addressed to the presidents of Ohio colleges and universities. The letter requests a report on..."
- Subject (FAST): "United States. National Youth Administration" -> "correspondence; education"
- transcript: "Federal Security Agency NATIONAL YOUTH ADMINISTRATION FOR OHIO Hoster Bldg. Columbus, Ohio" -> "Federal Security Agency NATIONAL YOUTH ADMINISTRATION FOR OHIO Hoster Bldg. Columbus, Ohio"
- transcript: "November 8, 1939" -> "November 8, 1939"
- transcript: "COLLEGE AID LETTER #4" -> "COLLEGE AID LETTER #4"
- transcript: "TO: Presidents of Ohio Colleges and Universities" -> "TO: Presidents of Ohio Colleges and Universities"
- transcript: "The Washington office of the National Youth Administration has requested a report on institution participation in the NYA College and Graduate Aid Program, including the following information:" -> "The Washington office of the National Youth Administration has requested a report on institution participation in the NYA College and Graduate Aid Program, including the follow- ing information:"

### BC-0710
- Title: "Letter to Mr. Murray Sheehan, 8 September 1941" -> "Letter to Mr. Murray Sheehan regarding Karoom Generdoomying's admission, 8 September 1941"
- Correspondents: "Mr. Murray Sheehan" -> "Sheehan, Murray"
- Location: "Massachusetts--Glouchester" -> "Ohio--Oxford"
- Summary: "A letter from Alfred H. Upham, president of Miami University (1928–1945), to Mr. Murray Sheehan, confirming the admission of Karoon Gengradomying as a freshman and mentioning other Thai students at the university." -> "A letter from Alfred H. Upham, president of Miami University (1928-1945), to Mr. Murray Sheehan, dated 8 September 1941. The letter confirms the admission of Karoom Generdoomying to Miami University as a freshman. Uph..."
- Subject (FAST): "Universities and colleges--Admission; international students" -> "correspondence; Miami University (Oxford, Ohio); international students"
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "Mr. Murray Sheehan Monsonhurst 59 Glouchester, Massachusetts" -> "Mr. Murray Sheehan Monsomhurst 59 Gloucaster, Massachusetts"
- transcript: "Dear Murray:" -> "Dear Murray:"
- transcript: "Replying to your letter of September 6, I can assure you that we shall be pleased to admit Karoon Gengradomying to Miami University as a freshman." -> "Replying to your letter of September 6, I can assure you that we shall be pleased to admit Karoom Generdoomying to Miami University as a freshman."
- transcript: "While of course we know nothing of the University you mention in Bangkok or of its entrance examinations, the other boys from Thailand have made such a good record here that we do not hesitate." -> "While of course we know nothing of the University you mention in Bangkok or of its entrance examinations, the other boys from Thailand have made such a good record here that we do not hesitate."
- transcript: "Freshman Week begins with a convocation next Sunday evening, September 14, but we can hold a room for him a little longer if necessary. We are trying to squeeze him into one of the freshman dormitories." -> "Freshman Week begins with a convocation next Sunday evening, September 14, but we can hold a room for him a little longer if necessary. We are trying to squeeze him into one of the freshman dormitories."

### BC-0711
- Title: "Letter to Mr. Murray Sheehan, 19 November 1941" -> "Letter to Mr. Murray Sheehan from the president, 19 November 1941"
- Correspondents: "Mr. Murray Sheehan" -> "Sheehan, Murray"
- Location: "District of Columbia--Washington" -> "District of Columbia--Washington; Ohio--Oxford"
- Summary: "A letter from Alfred H. Upham, president of Miami University (1928–1945), to Mr. Murray Sheehan, discussing the invitation of a Thai minister as a commencement speaker, highlighting concerns about international relati..." -> "A letter from Alfred H. Upham, president of Miami University (1928-1945), to Mr. Murray Sheehan at the Royal Thai Legation in Washington, D.C. Upham discusses the possibility of inviting a Thai minister to speak at th..."
- Subject (FAST): "international relations" -> "correspondence; Miami University (Oxford, Ohio); international students; Thailand"
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "I have just now got around to the problem of finding speakers for our Commencement exercises next June. Naturally I am greatly attracted by your suggestion that there is again a minister from Thai in Washington who wo..." -> "I have just now got around to the problem of finding speakers for our Commencement exercises next June. Naturally I am greatly attracted by your suggestion that there is again a minister from Thai in Washington who wo..."
- transcript: "Seriously, I should be glad to have you extend our invitation to the Minister to deliver the Commencement address to the graduates of Miami University on the morning of Monday, June 8, 1942, which is our regular Comme..." -> "Seriously, I should be glad to have you extend our in- vitation to the Minister to deliver the Commencement address to the graduates of Miami University on the morning of Monday, June 8, 1942, which is our regular Com..."
- transcript: "I had hoped for an occasion which would take me to Washington before this time. Unfortunately for me, the annual meeting of the National Association of State Universities was changed from Washington to Chicago because..." -> "I had hoped for an occasion which would take me to Washington before this time. Unfortunately for me, the annual meeting of the National Association of State Universities was changed from Washington to Chicago because..."
- transcript: "We greatly miss some of our friends among the Thailand boys who were with us last year. Those who are here at the present time, however, are giving an excellent account of themselves." -> "We greatly miss some of our friends among the Thailand boys who were with us last year. Those who are here at the present time, however, are giving an excellent account of them- selves."

### BC-0713
- Title: "Letter from M.R. Seni Pramoj to President A.H. Upham, 28 February 1942" -> "Letter from M.R. Seni Pramoj to A.H. Upham, 26 February 1942"
- Correspondents: "A.H. Upham" -> "Upham, Alfred H."
- Date: "1942-02-28" -> "1942-02-26"
- Summary: "A letter from M.R. Seni Pramoj to Mr. A.H. Upham, discussing the cancellation of an annual meeting of Thai students due to the war." -> "A letter from M.R. Seni Pramoj, Minister for Thailand, to Alfred H. Upham, president of Miami University, dated 26 February 1942. The letter expresses gratitude for Upham's offer to host the annual meeting of Thai stu..."
- Subject (FAST): "Thai students; World War (1939-1945); Miami University (Oxford, Ohio)" -> "correspondence; Miami University (Oxford, Ohio); Thai students; World War (1939-1945)"
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "RECEIVED MAR 2 1942" -> "[handwritten] RECEIVED [handwritten] MAR 2 1942"
- transcript: "February 28th, 1942." -> "February 26th, 1942."
- transcript: "[handwritten] Seni Pramoj" -> "[handwritten] M. R. Seni Pramoj"

### BC-0714
- Title: "Letter to Mr. Murray Sheehan from the President, 26 May 1942" -> "Letter to Mr. Murray Sheehan from the president, 26 May 1942"
- Correspondents: "Mr. Murray Sheehan" -> "Sheehan, Murray"
- Summary: "A letter from Alfred H. Upham, president of Miami University (1928–1945), to Mr. Murray Sheehan at the Royal Thai Legation, regarding plans for commencement and arrangements for Sheehan's visit." -> "A letter dated 26 May 1942 from Alfred H. Upham, president of Miami University (1928-1945), to Mr. Murray Sheehan of the Royal Thai Legation in Washington, D.C. The letter expresses delight at Sheehan's upcoming visit..."
- Subject (FAST): "Thailand" -> "correspondence; Miami University (Oxford, Ohio); Thailand"
- transcript: "I am delighted to know that you are coming on for Commencement. We shall all be glad to see you and I think you will find yourself very comfortable in David Swing Hall where we are making a reservation for you." -> "I am delighted to know that you are coming on for Commencement. We shall all be glad to see you and I think you will find yourself very comfortable in David Shing Hall where we are making a reservation for you."
- transcript: "It is too bad that we cannot have at least one boy from Thailand in the graduating class while you are here, particularly since we were unable to secure the Minister as our speaker." -> "It is too bad that we cannot have at least one boy from Thailand in the graduating class while you are here, particularly since we were unable to secure the Minister as our speaker."

### BC-0716
- Title: "Letter to President A. H. Upham from Royal Thai Legation, 2 June 1942" -> "Letter to President A. H. Upham from Muenay Shichan, 2 June 1942"
- Creator: "Royal Thai Legation" -> "Shichan, Muenay"
- Correspondents: "President A. H. Upham" -> ""
- Summary: "A letter from the Royal Thai Legation's Student Department to President A.H. Upham of Miami University expressing appreciation for hospitality and admiration for the university's work." -> "A letter from Muenay Shichan of the Royal Thai Legation's Students' Department to President Alfred H. Upham of Miami University, dated 2 June 1942. Shichan expresses gratitude for the hospitality received during a vis..."
- Subject (FAST): "Miami University (Oxford, Ohio); correspondence" -> "correspondence; Miami University (Oxford, Ohio); international students"
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "ROYAL THAI LEGATION STUDENT'S DEPARTMENT" -> "ROYAL THAI LEGATION STUDENTS' DEPARTMENT"
- transcript: "2300 KALORAMA ROAD WASHINGTON, D. C." -> "2300 KALORAMA ROAD WASHINGTON, D.C."
- transcript: "President A. H. Upham Miami University" -> "President A. H. Upham Miami University"
- transcript: "Just a line, upon my return to the Legation, to thank you for the many courtesies which were shown to me while I was at the University, and to tell you again how proud I am of the wonderful work which you are doing th..." -> "Just a line, upon my return to the Legation, to thank you for the many courtesies which were shown to me while I was at the University, and to tell you again how proud I am of the wonderful work which you are doing th..."
- transcript: "[handwritten] Murry [unclear]" -> "[handwritten] Muenay Shichan"

### BC-0718
- Contributors: "John W. Nason" -> ""
- Correspondents: "President A. H. Upham" -> "Upham, Alfred H."
- Summary: "A letter from C. V. Hibbard of the National Japanese American Student Relocation Council to President A. H. Upham of Miami University recommending Nisei students for deferment in quotas." -> "A letter from C. V. Hibbard, National Director of the National Japanese American Student Relocation Council, to Alfred H. Upham, president of Miami University. The letter discusses changes in the deferment policy for..."
- Subject (FAST): "Japanese American college students; United States. War Manpower Commission; United States. Selective Service System" -> "correspondence; Miami University (Oxford, Ohio); Japanese Americans; World War (1939-1945); United States. Selective Service System"
- Theme: "Japanese American education; World War II policies" -> ""
- Genre: "correspondence" -> "letters (correspondence)"
- Language: "English" -> ""
- transcript: "NATIONAL JAPANESE AMERICAN STUDENT RELOCATION COUNCIL" -> "NATIONAL JAPANESE AMERICAN STUDENT RELOCATION COUNCIL"
- transcript: "RITtenhouse 9378" -> "RITtenhouse 9372"
- transcript: "John W. Nason, National Chairman C. V. Hibbard, National Director" -> "John W. Nason, National Chairman C. V. Hibbard, National Director"
- transcript: "The War Manpower Commission in conjunction with the Selective Service System has recently changed the basis for the deferment of undergraduate students in Engineering, Physics, Chemistry, and similar subjects. Each co..." -> "The War Manpower Commission in conjunction with the Selective Service System has recently changed the basis for the deferment of undergraduate students in Engineering, Physics, Chemistry, and similar subjects. Each co..."
- transcript: "It has come to our attention that certain institutions are recommending Nisei students for deferment in their quotas. You may be interested in the statement of Dean Everett L. Hunt of Swarthmore College." -> "It has come to our attention that certain institutions are recommending Nisei students for deferment in their quotas. You may be interested in the statement of Dean Everett L. Hunt of Swarthmore College."

### BC-0897
- Title: "Letter from Harold V. Lucas to the President of Miami University, 24 April 1940" -> "Letter regarding Wing Kong Chong, 24 April 1940"
- Creator: "Lucas, Harold V." -> "Lucas, Harold W."
- Correspondents: "President of Miami University" -> ""
- Summary: "A letter from Harold V. Lucas to Alfred H. Upham, president of Miami University (1928–1945) providing a character reference for student Wing Kong Chong, highlighting his qualities as a future educator." -> "A letter from Harold W. Lucas, General Secretary of the YMCA, to the President of Miami University, dated April 24, 1940. The letter provides a personal note regarding Wing Kong Chong, a student at Miami University wh..."
- Subject (FAST): "education" -> "correspondence; Miami University (Oxford, Ohio); education"
- Language: "English" -> ""
- transcript: "[handwritten] Copy MIAMI UNIVERSITY OXFORD, OHIO" -> "[handwritten] Dear [handwritten] Miami University [handwritten] Oxford, Ohio"
- transcript: "" -> "MIAMI UNIVERSITY OXFORD, OHIO"
- transcript: "President Miami University" -> "President Miami University"
- transcript: "It has come to my attention that a personal note from me might well be added to your file dealing with the character and person of one of your students Wing Kong Chong who, I understand, hopes to be graduated from you..." -> "It has come to my attention that a personal note from me might well be added to your file dealing with the character and person of one of your students Wing Kong Chong who, I understand, hopes to be graduated from you..."
- transcript: "I knew Wing Kong when he was in High School and during a summer camp I came to know him even better. His character, I believe, is above reproach. His willingness to be helpful and his leadership even as a boy was very..." -> "I knew Wing Kong when he was in High School and during a summer camp I came to know him even better. His character, I believe, is above reproach. His willingness to be helpful and his leadership even as a boy was very..."

### BC-0926
- Title: "Financial assistance given to students and trainees from China, 20 September 1945" -> "Financial assistance for Chinese students and trainees, 20 September 1945"
- Summary: "Letter from the Department of State discussing financial aid and admission requirements for Chinese students in the U.S. dated September 20, 1945." -> "A letter from the United States Department of State dated 20 September 1945, discussing financial assistance for Chinese students and trainees. The letter addresses the handling of visa applications for Chinese nation..."
- Subject (FAST): "Chinese students" -> "correspondence; Chinese students; education"
- Genre: "correspondence" -> "letters (correspondence)"
- transcript: "" -> "[handwritten] F.13"
- transcript: "SAVINGS" -> ""
- transcript: "[handwritten] FLS" -> ""

### BC-0934
- Contributors: "Carol L. Anderson; Paul F. Erwin; Ernest H. Hahm" -> ""
- Correspondents: "Rose Choi" -> ""
- Summary: "A document outlining scholarship opportunities for a Korean student at Miami University, detailing housing, meals, and educational provisions." -> "This document outlines a scholarship opportunity offered by Miami University in Oxford, Ohio, for a Korean student named Soon Choi from Seoul, Korea. The scholarship includes room and board, meals, clothing, and livin..."
- Subject (FAST): "scholarships; foreign students; Korean students" -> "Miami University (Oxford, Ohio); international students; scholarships"
- Language: "English" -> ""
- transcript: "OFFER OF SCHOLARSHIP FOR KOREAN STUDENT" -> "[handwritten] Pres. Hahm"
- transcript: "Name of college offering opportunity -- Miami University" -> "OFF. OF SCHOLARSHIP FOR FOREIGN STUDENT Name of college offering opportunity -- Miami University"
- transcript: "Clothing and living expense provided by Kappa Phi Sorority and Wesley Foundation. Books and incidental college expenses paid by Foreign Student Committee. Provision for vacation and holiday periods -- Foreign Student..." -> "Clothing and living expense provided by Kappa Phi Sorority and Wesley Foundation. Books and incidental college expenses paid by Foreign Student Committee. Provisions for vacation and holiday periods -- Foreign Student..."
- transcript: "Conditions of scholarship -- read and speak English. Field of Study -- Arts and Science." -> "Conditions of scholarship -- road and speak English. Field of study -- Arts and Science."
- transcript: "Student Selected -- Rose Choi, 10-254 Yon Am-Dong, Seoul, Korea. We certify that this foreign student will not displace an American student." -> "Student selected -- Soon Choi, 18-254 Yon Am-Dong, Seoul, Korea."
