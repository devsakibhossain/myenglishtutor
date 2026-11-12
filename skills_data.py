"""
Comprehensive database of 200 Fast-Speech English Skills (Basic to Advanced).
Organized into 10 Modules of 20 skills each.
"""

MODULES = {
    1: "Super-Fast Sound Reductions & Contractions",
    2: "Connected Speech, Linking & Word Blending",
    3: "Weak Forms & Function Word Compressions",
    4: "High-Speed Thought Chunking & Fillers",
    5: "100 Essential Phrasal Verbs at Rapid Speed",
    6: "Everyday American Colloquial Slangs & Idioms",
    7: "High-Speed Freelance, Upwork & Client English",
    8: "Technical Analytics & Tracking Spoken Fluency",
    9: "Rapid Conversational Flow & Storytelling",
    10: "Elite Pronunciation & 180-WPM Speed Drills"
}

# 200 Skills Master Dictionary
SKILLS = [
    # Module 1: Reductions & Contractions (1-20)
    (1, 1, "Gonna (Going to)", "gonna", "I'm gonna push the GTM tag right now.", "ভবিষ্যতে কিছু করার ফাস্ট আমেরিকান রূপ।", "Say 5 times fast: I'm gonna do it, I'm gonna go."),
    (2, 1, "Wanna (Want to)", "wanna", "Do you wanna hop on a quick Zoom call?", "কোনো কিছু চাওয়ার বা অফার করার শর্টকাট।", "Say: Wanna grab lunch? Wanna see this?"),
    (3, 1, "Gotta (Got to / Have to)", "gotta", "I gotta bounce in five minutes.", "কোনো কাজ দ্রুত করার বাধ্যবাধকতা বোঝাতে।", "Say: I gotta go, you gotta see this."),
    (4, 1, "Kinda (Kind of)", "kinda", "It's kinda tricky with Safari ITP restrictions.", "কিছুটা বা খানিকটা বোঝাতে আমেরিকান ইনফরমাল রূপ।", "Say: It's kinda hard, kinda cool."),
    (5, 1, "Sorta (Sort of)", "sorta", "We're sorta waiting on the client's approval.", "এক প্রকার বা কিছুটা বোঝাতে ব্যবহৃত হয়।", "Say: I'm sorta tired, sorta busy."),
    (6, 1, "Shoulda (Should have)", "shoulda", "We shoulda enabled Consent Mode v2 earlier.", "অতীতে কোনো কাজ করা উচিত ছিল বোঝাতে।", "Say: We shoulda known, you shoulda called."),
    (7, 1, "Woulda (Would have)", "woulda", "That woulda broken the checkout tracking.", "অতীতে কোনো কিছু ঘটতে পারত কিন্তু ঘটেনি।", "Say: I woulda done it, that woulda worked."),
    (8, 1, "Coulda (Could have)", "coulda", "They coulda used a server-side container.", "অতীতের সামর্থ্য যা কাজে লাগানো হয়নি।", "Say: You coulda told me, we coulda won."),
    (9, 1, "Whaddya (What do you)", "whaddya", "Whaddya think about this attribution window?", "'What do you' এর সুপার-ফাস্ট ব্লেন্ডেড রূপ।", "Say: Whaddya mean? Whaddya want?"),
    (10, 1, "Dunno (Don't know)", "dunno", "I dunno why the purchase event is null.", "জানেন না বোঝাতে ক্যাজুয়াল আমেরিকান রূপ।", "Say: I dunno man, I dunno yet."),
    (11, 1, "Lemme (Let me)", "lemme", "Lemme share my screen real quick.", "অনুমতি নেওয়া বা নিজে কিছু শুরু করার ফাস্ট রূপ।", "Say: Lemme see, lemme check it."),
    (12, 1, "Gimme (Give me)", "gimme", "Gimme a sec to test this in preview mode.", "কোনো কিছু চাওয়ার দ্রুত ইনফরমাল রূপ।", "Say: Gimme that, gimme a minute."),
    (13, 1, "Outta (Out of)", "outta", "We're almost outta time on this sprint.", "কোনো কিছু শেষ হয়ে যাওয়া বা বাইরে যাওয়া।", "Say: Outta here, outta nowhere."),
    (14, 1, "Betcha (Bet you)", "betcha", "I betcha the transaction_id is missing.", "নিশ্চিতভাবে বাজি ধরে বলা।", "Say: I betcha he knows, betcha it works."),
    (15, 1, "Gotcha (I got you)", "gotcha", "Gotcha, I'll update the tag right away.", "কারো কথা বুঝেছি বোঝাতে সবচেয়ে জনপ্রিয় স্ল্যাং।", "Say: Ah gotcha! Gotcha covered."),
    (16, 1, "Hafta (Have to)", "hafta", "You hafta pass normalized email hashes.", "কোনো কিছু করতেই হবে বোঝাতে।", "Say: You hafta listen, we hafta go."),
    (17, 1, "Hasta (Has to)", "hasta", "The client hasta approve the milestone first.", "৩য় ব্যক্তি কাউকে কিছু করতে হবে বোঝাতে।", "Say: He hasta sign it, she hasta see it."),
    (18, 1, "Usta (Used to)", "usta", "We usta track via Universal Analytics.", "অতীতে নিয়মিত কিছু করা হতো বোঝাতে।", "Say: I usta live there, we usta play."),
    (19, 1, "Lotta (Lot of)", "lotta", "A lotta events are dropping attribution.", "অনেক বা প্রচুর বোঝাতে দ্রুত উচ্চারণ।", "Say: A lotta work, a lotta fun."),
    (20, 1, "C'mon (Come on)", "c'mon", "C'mon, let's wrap this up before 5 PM.", "কাউকে উৎসাহিত করা বা তাগাদা দেওয়া।", "Say: C'mon man, c'mon let's go."),

    # Module 2: Connected Speech & Blending (21-40)
    (21, 2, "Consonant to Vowel Linking", "Hold-on -> Hol-don", "Hold on, let me check it out.", "শব্দের শেষ ব্যঞ্জনবর্ণ পরের স্বরবর্ণের সাথে জোড়া লাগানো।", "Drill: Check-it-out, pick-it-up, turn-it-on."),
    (22, 2, "Intrusive /w/ Glide", "Go-(w)-on", "Go on and deploy the container.", "দুটি ভাওয়েল ধ্বনির মাঝে নরম /w/ ঢুকিয়ে দ্রুত বলা।", "Drill: Go-(w)-away, do-(w)-it, you-(w)-are."),
    (23, 2, "Intrusive /j/ Glide", "I-(y)-agree", "I agree with your marketing proposal.", "ভাওয়েলের পর /j/ ('ইয়') সাউন্ড যোগ করে মেলানো।", "Drill: See-(y)-it, say-(y)-it, he-(y)-is."),
    (24, 2, "Gemination (Twin Consonants)", "Black coffee -> Bla-coffee", "Grab a black coffee before the meeting.", "একই কনসোনেন্ট পাশাপাশি এলে একবার উচ্চারণ ধরে রাখা।", "Drill: Social life, bad dog, top post."),
    (25, 2, "T+Y Palatalization (/tʃ/)", "Meet you -> Mee-chu", "Nice to meet you on Zoom today.", "T এবং Y মিলিত হয়ে 'চ' বা /tʃ/ ধ্বনি হওয়া।", "Drill: Don't you (don-chu), what you (wha-chu)."),
    (26, 2, "D+Y Palatalization (/dʒ/)", "Did you -> Di-dju", "Did you check the server container logs?", "D এবং Y মিলিত হয়ে 'জ' বা /dʒ/ ধ্বনি হওয়া।", "Drill: Would you (wood-ju), could you (cood-ju)."),
    (27, 2, "Elision of final /t/", "Next week -> Nex-week", "Let's review the conversions next week.", "কনসোনেন্টের আগে শব্দের শেষের 'T' গিলে ফেলা।", "Drill: Last night -> Las-night, first day -> firs-day."),
    (28, 2, "Elision of final /d/", "Hold tight -> Hol-tight", "Hold tight while the GTM tags load.", "কনসোনেন্টের আগে 'D' ড্রপ করা।", "Drill: Stand there -> Stan-there, blind man -> blin-man."),
    (29, 2, "Nasal Assimilation", "Ten bucks -> Tem-bucks", "It costs ten bucks on Stape.", "N সাউন্ড B/P এর আগে M হয়ে যাওয়া।", "Drill: In Paris -> Im-Paris, one person -> wam-person."),
    (30, 2, "Glottal Stop before /n/", "Button -> Bu'n", "Click the purchase button on mobile.", "জিহ্বা ও গলা দিয়ে বাতাস আটকে T না বলা।", "Drill: Mountain -> Moun'n, curtain -> cur'n."),
    (31, 2, "American Flap-T Across Words", "Get out -> Ge-dout", "Get out of the preview debugger.", "শব্দের মাঝে বা শেষে T নরম D এর মতো ট্যাপ করা।", "Drill: Put it on -> Pu-di-don, wait a bit -> wai-də-bit."),
    (32, 2, "Schwa Compression in 3-Syllable Words", "Family -> Fam-lee", "I was discussing this with my family.", "মাঝখানের ভাওয়েল ড্রপ করে শব্দকে ২ সিলেবলে নামানো।", "Drill: Camera -> Cam-ra, chocolate -> choc-lit."),
    (33, 2, "Linking -R (British & Global)", "Four hours -> Four-r-hours", "The audit took four hours to complete.", "ভাওয়েলের আগে R সাউন্ড পরিষ্কার লিঙ্ক করা।", "Drill: Far away -> Fa-r-away, clear air -> clea-r-air."),
    (34, 2, "Silent Auxiliary Contraction", "What are you doing? -> Whatcha doin'?", "Whatcha doing with that Meta pixel?", "সাহায্যকারী ক্রিয়া চেপে সরাসরি 'ওয়াচা' বলা।", "Drill: Where are you going? -> Where ya goin'?"),
    (35, 2, "Dropped /h/ in Weak Pronouns", "Tell him -> Te-lim", "I'll tell him about the attribution fix.", "দুর্বল সর্বনাম থেকে H ড্রপ করে পূর্বের শব্দের সাথে মেলানো।", "Drill: Ask her -> As-ker, see him -> see-im."),
    (36, 2, "Reduction of 'And'", "Rock and roll -> Rock-n-roll", "Let's test cookies and parameters.", "'And' কে শুধু 'এন' বা 'ন' বানিয়ে ফেলা।", "Drill: Bread and butter, black and white."),
    (37, 2, "Reduction of 'Or'", "More or less -> More-er-less", "It's more or less identical to yesterday.", "'Or' কে দ্রুত 'আর' বা 'এর' উচ্চারণ করা।", "Drill: Two or three -> Two-er-three."),
    (38, 2, "Reduction of 'Than'", "Better than -> Bedder-n", "Server-side is better than client pixels.", "'Than' কে দ্রুত 'ন' বা 'দেন' বানিয়ে বলা।", "Drill: Faster than, bigger than."),
    (39, 2, "Fast Preposition Blending", "At the end of the day", "At the end of the day, ROAS is what matters.", "পুরো ফ্রেজকে এক নিশ্বাসে ১টি শব্দের মতো বলা।", "Drill: Say in 1 breath: At-the-end-of-the-day."),
    (40, 2, "Continuous Speech Sound Ribbon", "Sound Ribbon Technique", "We are testing the dataLayer push right now.", "শব্দে শব্দে না থেমে পুরো বাক্য গানের সুরের মতো জোড়া দেওয়া।", "Drill: Connect 6 words without taking a breath."),

    # Module 3: Weak Forms & Function Word Compressions (41-60)
    (41, 3, "Weak 'To' (/tə/)", "Want to -> Want-tə", "I need to configure this tag.", "'To' কে 'টু' না বলে সংক্ষেপে 'ত' বলা।", "Drill: Go to work, ready to start."),
    (42, 3, "Weak 'For' (/fər/)", "For you -> Fər-you", "This report is for your marketing team.", "'For' কে 'ফর' না বলে দ্রুত 'ফার' বলা।", "Drill: Wait for me, good for you."),
    (43, 3, "Weak 'Can' (/kən/)", "I can do it -> I kən do it", "I can verify your GA4 setup today.", "হ্যাঁ-বোধক can হবে দুর্বল (/kən/), না-বোধক can't হবে জোরদার (/kænt/).", "Drill: I can do it, but I can't stay."),
    (44, 3, "Weak 'From' (/frəm/)", "From -> Frəm", "Where is this traffic coming from?", "'From' কে 'ফ্রম' না বলে দ্রুত 'ফ্রাম' বলা।", "Drill: Away from home, back from lunch."),
    (45, 3, "Weak 'At' (/ət/)", "Look at that -> Loo-kət that", "Look at that event match score.", "'At' কে 'অ্যাট' না বলে সংক্ষেপে 'অত' বলা।", "Drill: Meet at nine, stay at home."),
    (46, 3, "Weak 'That' (/ðət/)", "The tag that fired", "The tag that fired had missing currency.", "রিলেটিভ 'that' হবে দুর্বল (/ðət/)।", "Drill: The plan that worked."),
    (47, 3, "Weak 'Them' (/əm/)", "Check them -> Che-kəm", "Open the logs and check them now.", "'Them' থেকে Th বাদ দিয়ে 'আম' বলা।", "Drill: Send them, fix them, show them."),
    (48, 3, "Weak 'You' (/jə/)", "See you -> See-yə", "See you on the call tomorrow.", "'You' কে দ্রুত ক্যাজুয়ালি 'ইয়া' বলা।", "Drill: Love you, thank you, call you."),
    (49, 3, "Weak 'Your' (/jər/)", "Your name -> Yər-name", "What's your preferred time for the sync?", "'Your' কে 'ইউর' না বলে 'ইয়ার' বলা।", "Drill: Take your time, bring your laptop."),
    (50, 3, "Weak 'Him' (/ɪm/)", "Help him -> Hel-pɪm", "I helped him set up the Stape container.", "H বাদ দিয়ে সোজা আগের কনসোনেন্টের সাথে জোড়া।", "Drill: Call him, tell him, ask him."),
    (51, 3, "Weak 'Her' (/ər/)", "Call her -> Cal-lər", "I sent her the completed proposal.", "H বাদ দিয়ে 'আর' হিসেবে মেলানো।", "Drill: Message her, pay her, see her."),
    (52, 3, "Weak 'Have' (/əv/)", "They have -> They-əv", "They have already approved the contract.", "'Have' কে সংক্ষেপে 'অভ' বা 'ভ' বলা।", "Drill: We have done it, could have known."),
    (53, 3, "Weak 'Has' (/əz/)", "It has -> It-əz", "It has been working flawlessly.", "'Has' কে সংক্ষেপে 'আজ' বলা।", "Drill: Time has come, he has left."),
    (54, 3, "Weak 'Had' (/əd/)", "We had -> We-əd", "We had tested the pixel earlier.", "'Had' কে সংক্ষেপে 'অ্যাড' বলা।", "Drill: They had finished, I had seen."),
    (55, 3, "Weak 'Do' (/də/)", "How do you -> How-də-you", "How do you calculate your blended CPA?", "'Do' কে 'ডু' না বলে সংক্ষেপে 'দা' বলা।", "Drill: What do they do?"),
    (56, 3, "Weak 'Does' (/dəz/)", "What does it -> What-dəz-it", "What does this error code mean?", "'Does' কে দ্রুত 'ডাজ' বলা।", "Drill: How does it work?"),
    (57, 3, "Weak 'As' (/əz/)", "As fast as -> Az-fast-əz", "We will resolve this as fast as possible.", "'As' কে 'অ্যাজ' না বলে দ্রুত 'আজ' বলা।", "Drill: As good as new, as soon as possible."),
    (58, 3, "Weak 'Some' (/səm/)", "Some -> Səm", "Could you share some details?", "'Some' কে 'সাম' না বলে সংক্ষেপে 'সাম' বলা।", "Drill: Have some coffee."),
    (59, 3, "Weak 'Must' (/məs/)", "You must -> You-məs", "You must be very proud of these results.", "কনসোনেন্টের আগে T বাদ দিয়ে 'মাস' বলা।", "Drill: You must be joking."),
    (60, 3, "Weak 'Of' (/ə/)", "Piece of cake -> Piece-ə-cake", "Fixing this tracking bug is a piece of cake.", "কনসোনেন্টের আগে F বাদ দিয়ে শুধু 'আ' বলা।", "Drill: Cup of tea, out of time."),

    # Module 4: High-Speed Thought Chunking & Fillers (61-80)
    (61, 4, "I mean...", "I mean...", "I mean, we could also route via Cloudflare.", "কথা বলার মাঝে আটকে না গিয়ে ন্যাচারালভাবে নতুন চিন্তা আনা।", "Use when pivoting to a better idea."),
    (62, 4, "You know...", "You know...", "It's all about privacy compliance, you know.", "বায়ারের মনোযোগ ধরে রাখা ও মত নেওয়া।", "Use at the end of a point."),
    (63, 4, "To be honest...", "To be honest...", "To be honest, the current pixel setup is fragile.", "সাহসী কিন্তু ভদ্রভাবে সত্য তুলে ধরা।", "Use when giving honest technical audit."),
    (64, 4, "At the end of the day...", "At the end of the day...", "At the end of the day, conversions drive profit.", "মূল সিদ্ধান্তে আসার জন্য।", "Use when summarizing the bottom line."),
    (65, 4, "The thing is...", "The thing is...", "The thing is, Shopify checkout is sandboxed.", "আসল বাধা বা জটিলতা বোঝাতে।", "Use when introducing the core problem."),
    (66, 4, "As far as I'm concerned...", "As far as I'm concerned...", "As far as I'm concerned, Stape is the easiest fix.", "দৃঢ় পেশাদার মতামত প্রকাশ করতে।", "Use when giving a firm opinion."),
    (67, 4, "Basically...", "Basically...", "Basically, we need to match the event_id tokens.", "কঠিন কথাকে এক বাক্যে সংক্ষেপ করতে।", "Use when summarizing complex code."),
    (68, 4, "Literally...", "Literally...", "The tag literally fired five times per click.", "কোনো বিষয়ের ওপর জোর দিতে।", "Use to emphasize an exact occurrence."),
    (69, 4, "Pretty much...", "Pretty much...", "The container setup is pretty much complete.", "প্রায় সম্পূর্ণ হয়েছে বোঝাতে।", "Use when work is 95% done."),
    (70, 4, "In a nutshell...", "In a nutshell...", "In a nutshell, we're fixing data attribution loss.", "এক নজরে সারাংশ প্রকাশ করতে।", "Use for executive summaries."),
    (71, 4, "Off the top of my head...", "Off the top of my head...", "Off the top of my head, it should take 4 hours.", "মুহূর্তেই আনুমানিক হিসাব দিতে।", "Use for quick estimates."),
    (72, 4, "For the most part...", "For the most part...", "For the most part, the tags are firing correctly.", "অধিকাংশ ক্ষেত্রেই কাজ করছে বোঝাতে।", "Use to describe general performance."),
    (73, 4, "More or less...", "More or less...", "The numbers match more or less with Shopify.", "মোটামুটি কাছাকাছি বোঝাতে।", "Use when numbers are within 2-3%."),
    (74, 4, "If you ask me...", "If you ask me...", "If you ask me, we should migrate to server GTM.", "পরামর্শ দেওয়ার প্রফেশনাল ভূমিকা।", "Use before offering strategic advice."),
    (75, 4, "Long story short...", "Long story short...", "Long story short, we recovered 25% lost sales.", "অপ্রয়োজনীয় বিস্তারিত বাদ দিয়ে সোজা রেজাল্ট বলা।", "Use when skipping background details."),
    (76, 4, "All things considered...", "All things considered...", "All things considered, the campaign was a success.", "সবকিছু বিবেচনা করে সারমর্ম টানা।", "Use when concluding a project."),
    (77, 4, "To put it simply...", "To put it simply...", "To put it simply, clean data saves ad spend.", "জটিল টেকনিক্যাল কথাকে সহজ বিজনেসের ভাষায় রূপান্তর।", "Use when talking to non-tech founders."),
    (78, 4, "Truth be told...", "Truth be told...", "Truth be told, third-party cookies are dying.", "স্বচ্ছ ও খাঁটি সত্য বোঝাতে।", "Use to build deep client trust."),
    (79, 4, "Having said that...", "Having said that...", "Having said that, we still need client-side backup.", "আগের কথার সাথে নতুন বিপরীত পয়েন্ট যোগ করতে।", "Use as a smooth conversational pivot."),
    (80, 4, "By and large...", "By and large...", "By and large, our ad tracking is solid now.", "সামগ্রিকভাবে সবকিছু ঠিকঠাক বোঝাতে।", "Use for overall health status."),

    # Module 5: 100 Essential Phrasal Verbs at Rapid Speed (81-100)
    (81, 5, "Touch base", "Touch base", "Let's touch base on Friday to review ROAS.", "সংক্ষেপে যোগাযোগ করা বা আপডেট নেওয়া।", "Say: Let's touch base next week."),
    (82, 5, "Loop in", "Loop in", "I'll loop in our lead developer on Slack.", "কারো সাথে পরিচয় করিয়ে দেওয়া বা চ্যাটে যুক্ত করা।", "Say: Loop me in on that email."),
    (83, 5, "Circle back", "Circle back", "Let's circle back once the tags populate data.", "পরে আবার এই বিষয়ে কথা বলা।", "Say: We can circle back tomorrow."),
    (84, 5, "Wrap up", "Wrap up", "Let's wrap up this meeting in 2 minutes.", "কাজ বা মিটিং সুন্দরভাবে শেষ করা।", "Say: Time to wrap things up."),
    (85, 5, "Figure out", "Figure out", "I'll figure out why the deduplication dropped.", "গবেষণা বা চিন্তা করে সমাধান বের করা।", "Say: We gotta figure this out."),
    (86, 5, "Turn out", "Turn out", "It turned out to be a simple caching issue.", "কোনো ঘটনার চূড়ান্ত ফলাফল এমন হওয়া।", "Say: Everything turned out great."),
    (87, 5, "Drop off", "Drop off", "Our checkout conversion rate dropped off.", "সংখ্যা বা হার হঠাৎ কমে যাওয়া।", "Say: Traffic dropped off sharply."),
    (88, 5, "Catch up", "Catch up", "Great catching up on Zoom today!", "কারো সাথে কথা বলে আগের সব খোঁজ নেওয়া।", "Say: Let's catch up soon."),
    (89, 5, "Call off", "Call off", "They decided to call off the meeting.", "কোনো কিছু বাতিল ঘোষণা করা।", "Say: Don't call off the launch."),
    (90, 5, "Put off", "Put off", "We shouldn't put off this tracking audit.", "কোনো কাজ ফেলে রাখা বা স্থগিত করা।", "Say: Don't put it off till tomorrow."),
    (91, 5, "Kick off", "Kick off", "We are kicking off the GTM container setup.", "উৎসাহের সাথে কোনো প্রজেক্ট শুরু করা।", "Say: The project kicks off today."),
    (92, 5, "Wind down", "Wind down", "I'm winding down my work for the day.", "সারাদিনের কাজ আস্তে আস্তে গুটিয়ে আনা।", "Say: Winding down for the weekend."),
    (93, 5, "Sign off on", "Sign off on", "The client signed off on the final milestone.", "অফিসিয়ালি অনুমোদন দেওয়া বা সই করা।", "Say: Can you sign off on this?"),
    (94, 5, "Back out of", "Back out of", "They backed out of the agreement at the last min.", "প্রতিশ্রুতি দিয়েও শেষ মুহূর্তে সরে যাওয়া।", "Say: It's too late to back out."),
    (95, 5, "Blow away", "Blow away", "The tracking accuracy completely blew them away.", "কাউকে দারুণ পারফরম্যান্সে মুগ্ধ করে ফেলা।", "Say: Your work blew me away."),
    (96, 5, "Cut down on", "Cut down on", "We need to cut down on redundant HTTP requests.", "খরচ বা অপচয় কমিয়ে আনা।", "Say: Cut down on ad waste."),
    (97, 5, "Look forward to", "Look forward to", "Looking forward to working with your team!", "ভবিষ্যতের কোনো কাজের জন্য অধীর আগ্রহে অপেক্ষা করা।", "Say: Looking forward to the results."),
    (98, 5, "Run into", "Run into", "We ran into an unexpected CSP header restriction.", "অপ্রত্যাশিত বাধার সম্মুখীন হওয়া।", "Say: Ran into a quick issue."),
    (99, 5, "Give up on", "Give up on", "Don't give up on client-side pixels just yet.", "কোনো কিছুর ওপর আশা ছেড়ে দেওয়া।", "Say: Never give up on tracking."),
    (100, 5, "Pick up on", "Pick up on", "I picked up on their hesitation regarding cost.", "কারো অব্যক্ত মনোভাব বা ইঙ্গিত চট করে ধরে ফেলা।", "Say: Did you pick up on that?"),

    # Module 6: Everyday American Colloquial Slangs & Idioms (101-120)
    (101, 6, "I'm beat", "I'm beat", "Man, after five hours of debugging, I'm beat!", "চরমভাবে ক্লান্ত হয়ে পড়া।", "Say: I'm beat, going to bed."),
    (102, 6, "No sweat!", "No sweat!", "Thanks for fixing the tag! — No sweat, anytime!", "কোনো ব্যাপারই না / স্বাগতম।", "Say: No sweat man, glad to help!"),
    (103, 6, "Call it a day", "Call it a day", "Let's call it a day and resume tomorrow morning.", "আজকের মতো কাজ সমাপ্ত ঘোষণা করা।", "Say: Let's call it a day!"),
    (104, 6, "Ballpark figure", "Ballpark figure", "A ballpark figure for this audit is around $500.", "আনুমানিক খরচের ধারণা দেওয়া।", "Say: Give me a ballpark figure."),
    (105, 6, "Up in the air", "Up in the air", "The holiday ad budget is still up in the air.", "এখনও চূড়ান্ত হয়নি বা ঝুলন্ত অবস্থায় আছে।", "Say: Everything is up in the air."),
    (106, 6, "Cut corners", "Cut corners", "Don't cut corners on your server infrastructure.", "সস্তা বা খারাপ উপায়ে কাজ করে বিপদ ডেকে আনা।", "Say: Never cut corners on tracking."),
    (107, 6, "Hit the books", "Hit the books", "Time to hit the books and master BigQuery SQL.", "মনোযোগ দিয়ে পড়ালেখা বা স্টাডি শুরু করা।", "Say: Gotta hit the books tonight."),
    (108, 6, "Cost an arm and a leg", "Cost an arm and a leg", "Some enterprise analytics platforms cost an arm and a leg.", "প্রচণ্ড চড়া দাম হওয়া।", "Say: That tool costs an arm and a leg."),
    (109, 6, "Piece of cake", "Piece of cake", "Configuring Google Ads enhanced conversions is a piece of cake.", "খুবই সহজ বা পানসে কাজ।", "Say: It was a piece of cake!"),
    (110, 6, "Under the weather", "Under the weather", "I was feeling a bit under the weather yesterday.", "হালকা অসুস্থ বা দুর্বল লাগা।", "Say: Feeling under the weather today."),
    (111, 6, "Bite the bullet", "Bite the bullet", "We had to bite the bullet and upgrade our servers.", "অনিচ্ছা সত্ত্বেও কঠিন সিদ্ধান্ত মেনে নেওয়া।", "Say: Time to bite the bullet."),
    (112, 6, "Break the ice", "Break the ice", "A quick joke breaks the ice before business talks.", "কথোপকথনের শুরুতে জড়তা কাটানো।", "Say: Let's break the ice."),
    (113, 6, "Spill the tea", "Spill the tea", "Come on, spill the tea on their new marketing campaign!", "ভেতরের গোপন বা আকর্ষণীয় খবর ফাঁস করা।", "Say: Spill the tea!"),
    (114, 6, "Pull someone's leg", "Pull someone's leg", "Don't worry, I'm just pulling your leg!", "কাউকে নিয়ে মজা বা কৌতুক করা।", "Say: You're pulling my leg!"),
    (115, 6, "Pitch in", "Pitch in", "Everyone pitched in to hit the project deadline.", "সবাই মিলে একযোগে সাহায্য করা।", "Say: Let's all pitch in."),
    (116, 6, "On the fence", "On the fence", "The client is on the fence between Stape and GCP.", "সিদ্ধান্তহীনতায় দ্বিধায় থাকা।", "Say: I'm still on the fence."),
    (117, 6, "Ring a bell", "Ring a bell", "Does that error message ring a bell?", "আগে শোনা বা চেনা চেনা লাগা।", "Say: That name rings a bell."),
    (118, 6, "Rule of thumb", "Rule of thumb", "As a rule of thumb, always test in preview mode.", "অভিজ্ঞতা থেকে পাওয়া সাধারণ সোনালী নিয়ম।", "Say: Good rule of thumb."),
    (119, 6, "Play it by ear", "Play it by ear", "Let's see how traffic flows and play it by ear.", "আগে থেকে প্ল্যান না করে পরিস্থিতি অনুযায়ী সিদ্ধান্ত নেওয়া।", "Say: Let's play it by ear."),
    (120, 6, "See eye to eye", "See eye to eye", "We see eye to eye on the tracking strategy.", "একে অপরের সাথে সম্পূর্ণ একমত হওয়া।", "Say: We see eye to eye."),

    # Module 7: High-Speed Freelance, Upwork & Client Call English (121-140)
    (121, 7, "The 30-Second Elevator Pitch", "The Elevator Pitch", "I specialize in server-side attribution and signal recovery.", "৩০ সেকেন্ডে নিজের মূল যোগ্যতা বায়ারের সামনে তুলে ধরা।", "Say: I help ecommerce brands recover 25% lost ad sales."),
    (122, 7, "Pricing Justification Architecture", "Pricing Justification", "Our fee covers infrastructure setup that saves $5,000 in ad waste.", "রেটকে ক্লায়েন্টের আর্থিক লাভের সাথে তুলনা করে প্রমাণ করা।", "Say: Clean data pays for itself in 30 days."),
    (123, 7, "Defending $60/hr Rate Jump", "Defending Rate", "The reason for my updated rate is that I specialize strictly in server signal recovery.", "নিজের স্পেশালাইজেশন দেখিয়ে রেট বাড়ানো।", "Say: I focus exclusively on high-ROI tracking infrastructure."),
    (124, 7, "Acknowledging Client Delays Without Blame", "No-Blame Delay Script", "No worries at all on the delay, I know how busy product launches get.", "বায়ার দেরি করলে দোষ না দিয়ে সহানুভূতি প্রকাশ করা।", "Say: Completely understand, let me know when you're ready."),
    (125, 7, "Clarifying Scope Creep Politely", "Scope Creep Defense", "I'd love to help with the other 4 domains! Let's spin up an add-on milestone.", "অতিরিক্ত কাজ ভদ্রভাবে আলাদা পেইড মাইলস্টোনে রূপান্তর।", "Say: That's outside our initial scope, but I can add a milestone."),
    (126, 7, "Explaining Tracking Bugs Without Fear", "Calm Bug Explanation", "The drop is caused by an unmapped dataLayer event, which is an easy 15-minute fix.", "ভয় না পেয়ে শান্ত ভঙ্গিতে সমস্যার কারণ ও সহজ সমাধানের কথা বলা।", "Say: Rest assured, this is very straightforward to resolve."),
    (127, 7, "Apologizing Without Losing Power", "Action-First Apology", "Thanks for pointing that out! I'm pushing the corrected payload right now.", "'I am sorry' বারবার না বলে অ্যাকশন নেওয়া।", "Say: Good catch, I'm already on it."),
    (128, 7, "Asking for 5-Star Reviews & Upwork Feedback", "High-Response Feedback Script", "If you're happy with the tracking accuracy, a quick 5-star review would mean the world!", "কাজের প্রশংসা পাওয়ার পর ভদ্রভাবে রিভিউ চাওয়া।", "Say: A short review helps my Upwork profile tremendously."),
    (129, 7, "Upselling Monthly Retainers", "Monthly Retainer Pitch", "Since Shopify updates themes frequently, a 5-hour monthly retainer keeps your tags verified.", "এককালীন কাজকে মাসিক চুক্তিতে রূপান্তর করা।", "Say: We can monitor your tracking health every single month."),
    (130, 7, "Scheduling Fast Follow-Ups", "Low-Friction Scheduling", "Are you free for a quick 10-minute sync tomorrow afternoon?", "সহজে ক্যালেন্ডার বুকিং নিশ্চিত করা।", "Say: Let's do a 10-minute sync on Thursday."),
    (131, 7, "Live Screen Share Walkthroughs", "Screen Share Guide", "As you can see right here on line 14 of Tag Assistant, the purchase event is firing.", "স্ক্রিন শেয়ার করে ক্লায়েন্টকে পয়েন্ট বুঝিয়ে দেওয়া।", "Say: Follow my cursor right here on the summary tab."),
    (132, 7, "Handling Deadline Crunches", "Deadline Prioritization", "To hit tomorrow's launch, let's prioritize the purchase tag and finish leads later.", "চাপের মুখে সবচেয়ে গুরুত্বপূর্ণ কাজটি আগে ডেলিভারি দেওয়া।", "Say: Let's lock in the purchase event first."),
    (133, 7, "Negotiating Milestone Release", "Milestone Release Request", "All tags are tested and live! Whenever you're ready, please release the milestone.", "পেমেন্ট রিলিজের জন্য শালীন অনুরোধ।", "Say: Feel free to approve the escrow milestone at your convenience."),
    (134, 7, "Communicating Holiday Schedules", "Holiday Notice", "Just a heads-up that I will be traveling this weekend, but fully reachable by email.", "আগে থেকেই ছুটির বিষয়ে বায়ারকে নোটিশ দেওয়া।", "Say: Giving you a quick heads-up about my availability."),
    (135, 7, "Resolving Payment & Invoicing Disputes", "Neutral Diplomacy", "Let's review the original scope document together to ensure we're both aligned.", "রাগ না করে ডকুমেন্টে ফিরে গিয়ে বিরোধ মেটানো।", "Say: Let's check our contract deliverables together."),
    (136, 7, "Setting Working Hours & Async Boundaries", "Async Boundaries", "I work async between 9 AM and 6 PM EST and respond to all messages within 2 hours.", "সারারাত সজাগ না থেকে কাজের সময় বেঁধে দেওয়া।", "Say: I do deep work in the morning and review tags in the afternoon."),
    (137, 7, "Explaining Deliverables in Plain English", "Translating JSON", "This setup means Meta knows exactly which ad generated each dollar.", "কোড না দেখিয়ে সরাসরি ডলার বা সেলস দেখানো।", "Say: You now have 100% visibility on your ad spend."),
    (138, 7, "Summarizing Next Steps on Zoom", "Next Steps Recap", "Action items: I will deploy the container, and you will share viewer access to GA4.", "মিটিং শেষে কে কী করবে স্পষ্ট করা।", "Say: Quick recap of our next steps."),
    (139, 7, "Delivering Post-Launch QA Reports", "Loom QA Walkthrough", "I recorded a 2-minute Loom video walking through the live purchase test.", "লুম ভিডিও দিয়ে বিশ্বাসযোগ্য ডেলিভারি দেওয়া।", "Say: Check this short video proof of the purchase event."),
    (140, 7, "Closing Deals with Indecisive Buyers", "Ethical Urgency", "I have one availability slot left this week if we can kick off today.", "সিদ্ধান্তহীন বায়ারকে আজই শুরু করতে রাজি করানো।", "Say: If you want this live before the weekend, let's start now."),

    # Module 8: Technical Web Analytics & Tracking Spoken Fluency (141-160)
    (141, 8, "Explaining GTM Server-Side Containers", "Server GTM Explanation", "Moving tags from the user's browser to an isolated cloud container.", "ক্লাউড কন্টেইনারের কার্যকারিতা মুখে বলা।", "Say: Server GTM runs on your own domain."),
    (142, 8, "Meta CAPI Deduplication Mechanics", "CAPI Deduplication", "Matching identical event_id hashes between browser and server.", "ডাবল কাউন্টিং বন্ধ করার মেকানিজম।", "Say: When event_id tokens match, Meta deduplicates the sale."),
    (143, 8, "GA4 Attribution Windows (7-Day vs 1-Day)", "Attribution Windows", "Comparing 7-day click vs 1-day view attribution models.", "অ্যাট্রিবিউশন উইন্ডোর পার্থক্য মুখে ব্যাখ্যা।", "Say: Meta uses a 7-day click window by default."),
    (144, 8, "Safari ITP & Cookie Lifetime Restrictions", "Safari ITP Capping", "Apple's WebKit restricts JavaScript cookies to 24 hours.", "আইটিপি ও কুকি মেয়াদের সমস্যা বোঝানো।", "Say: Safari ITP wipes client cookies after 24 hours."),
    (145, 8, "First-Party vs Third-Party Cookies", "Cookie Origin Scoping", "First-party cookies live on your custom domain, making them immune to blockers.", "ফার্স্ট পার্টি বনাম থার্ড পার্টির সুবিধা বোঝানো।", "Say: First-party cookies are set by your server."),
    (146, 8, "Deploying on GCP vs Stape.io", "GCP vs Stape Comparison", "Stape offers managed convenience; GCP provides complete enterprise ownership.", "ক্লাউড প্রোভাইডার তুলনা।", "Say: Stape is faster to deploy, GCP scales indefinitely."),
    (147, 8, "Event Match Quality (EMQ 8.0+)", "EMQ Optimization", "Passing normalized SHA-256 hashed customer parameters.", "ম্যাচ কোয়ালিটি স্কোর বাড়ানোর উপায়।", "Say: Email, phone, and IP hashes give an 8.5 EMQ score."),
    (148, 8, "Consent Mode v2 Implementation", "Consent Mode v2", "Adjusting Google tags dynamically based on user cookie banner consent.", "ইউরোপীয় আইন ও কনসেন্ট মোড ব্যাখ্যা।", "Say: Consent Mode v2 regulates ad_storage signals."),
    (149, 8, "BigQuery Export & Blended ROAS", "BigQuery Export", "Exporting raw GA4 events into BigQuery for true multi-touch attribution.", "বিগকোয়েরি ডাটা পাইপলাইন মুখে বলা।", "Say: BigQuery gives un-sampled row-level event data."),
    (150, 8, "DebugView & Tag Assistant QA", "DebugView Protocol", "Verifying live incoming event streams in real time.", "রিয়েলটাইম টেস্টিং প্রোটোকল।", "Say: Let's verify the purchase parameters in DebugView."),
    (151, 8, "User-ID Cross-Device Stitching", "User-ID Stitching", "Stitching mobile and desktop sessions to a single logged-in customer.", "ক্রস ডিভাইস ট্র্যাকিং বোঝানো।", "Say: User-ID connects the user journey across devices."),
    (152, 8, "Data Redaction & GDPR Compliance", "Data Redaction", "Stripping query parameter PII before hitting Google servers.", "ইউজার প্রাইভেসি ও পিআইআই ফিল্টারিং।", "Say: We redact emails from URLs to stay GDPR-compliant."),
    (153, 8, "Shopify E-commerce dataLayer Pushes", "dataLayer Pushes", "Pushing ecommerce items arrays with price, currency, and variant IDs.", "ডাটালেয়ার অবজেক্ট ব্যাখ্যা।", "Say: The dataLayer carries the items array and order total."),
    (154, 8, "Offline Conversion Import via CallRail", "Offline Conversion Import", "Matching dynamic number insertion phone calls back to Google Ads clicks.", "কল ট্র্যাকিং কনভার্সন ইমপোর্ট।", "Say: CallRail matches telephone calls to the gclid."),
    (155, 8, "Cross-Domain Measurement Configuration", "Cross-Domain Linking", "Preserving the _ga linker parameter across separate checkout domains.", "ক্রস ডোমেইন লিঙ্কার ব্যাখ্যা।", "Say: Cross-domain prevents session splitting on checkout."),
    (156, 8, "Custom Dimension Scoping (Event vs User)", "Dimension Scoping", "Assigning event-scoped parameters vs user-scoped properties.", "কাস্টম ডাইমেনশনের স্কোপিং মুখে বলা।", "Say: Event scope applies to single actions, user scope persists."),
    (157, 8, "Enhanced Conversions for Google Ads", "Enhanced Conversions", "Sending hashed customer data to Google Ads for post-cookie attribution.", "গুগল এনহ্যান্সড কনভার্সন।", "Say: Enhanced conversions recover modeled conversion data."),
    (158, 8, "Server-Side Proxy & Custom Subdomain", "Custom Subdomain Routing", "Routing server traffic through metrics.yourdomain.com.", "কাস্টম সাবডোমেন প্রক্সি।", "Say: A custom subdomain gives first-party context."),
    (159, 8, "Campaign UTM Standardization Architecture", "UTM Standardization", "Standardizing source, medium, campaign, and term naming conventions.", "ইউটিএম প্যারামিটার স্ট্যান্ডার্ডাইজেশন।", "Say: Consistent UTMs prevent unassigned traffic in GA4."),
    (160, 8, "Blended ROAS vs Marketing Efficiency Ratio (MER)", "Blended ROAS vs MER", "Comparing individual channel ROAS against total store revenue divided by ad spend.", "এমইআর বনাম ব্লেন্ডেড আরওএএস।", "Say: MER measures overall top-line marketing efficiency."),

    # Module 9: Rapid Conversational Flow, Banter & Storytelling (161-180)
    (161, 9, "The 3-Second Hook", "The 3-Second Hook", "You won't believe what broke their Shopify checkout yesterday.", "শুরুতেই চমকপ্রদ কথা বলে মনোযোগ কেড়ে নেওয়া।", "Say: Check this out, this is crazy."),
    (162, 9, "Setting High-Stakes Narrative", "High Stakes", "They were spending $10k a day with completely blind attribution.", "গল্পের ভেতরে আকর্ষণ ও উত্তেজনা তৈরি করা।", "Say: The stakes were massive on Black Friday."),
    (163, 9, "Direct Dialogue Quotation", "He was like... and I was like...", "He was like 'Our ads are failing!', and I was like 'Check your GTM.'", "নেটিভদের মতো সরাসরি উক্তি দিয়ে কথোপকথন বর্ণনা।", "Say: And I was like, let me check the container."),
    (164, 9, "Past Continuous for Scene Setting", "I was auditing when...", "I was auditing the checkout tags when the error popped up.", "দৃশ্যপট তৈরি করার জন্য পাস্ট কন্টিনিউয়াস টেন্স।", "Say: I was testing the container when it fired."),
    (165, 9, "Acceleration on Climax", "Speeding Up Speech", "And boom—the server tag caught the payload in milliseconds!", "উত্তেজনার মুহূর্তে দ্রুত কথা বলা।", "Say: And boom, conversions started flowing!"),
    (166, 9, "Deceleration on Key Takeaways", "Slowing Down Speech", "And that... is why first-party cookies... are non-negotiable.", "গুরুত্বপূর্ণ শিক্ষণীয় পয়েন্টে আস্তে স্পষ্ট করে বলা।", "Say: And that... changed everything."),
    (167, 9, "Self-Deprecating Humor", "Self-Deprecation", "I spent two hours debugging only to realize my ad blocker was on!", "নিজের ছোট ভুল নিয়ে হেসে বন্ধুত্ব তৈরি করা।", "Say: Can you believe I forgot to turn off my VPN?"),
    (168, 9, "Empathetic Agreement", "Totally / 100%", "Totally! That Shopify checkout update caught everyone off guard.", "বায়ারের কথার সাথে আন্তরিক সমর্থন দেওয়া।", "Say: 100%, tell me about it!"),
    (169, 9, "Playful Disagreement", "No way! / Are you serious?", "No way! Did Meta really reject that catalog feed?", "মজার ছলে অবাক হয়ে দ্বিমত বা বিস্ময় প্রকাশ।", "Say: Are you serious right now?"),
    (170, 9, "Redirecting Awkward Topics", "Smooth Topic Pivot", "Speaking of attribution, let me show you this new report.", "অস্বস্তিকর প্রসঙ্গ থেকে কৌশলে কাজের কথায় ফেরা।", "Say: Speaking of which, let's look at the tags."),
    (171, 9, "Answering Without Over-Explaining", "Concise Confidence", "Yes, that's already taken care of in the latest version.", "অতিরিক্ত কথা না বলে সংক্ষেপে আত্মবিশ্বাস দেখানো।", "Say: Yes, consider it done."),
    (172, 9, "Echo Questions", "Echo Questioning", "They dropped 40%? When did that start happening?", "অন্যের কথা পুনরাবৃত্তি করে কথা এগিয়ে নেওয়া।", "Say: Stape is down? Since when?"),
    (173, 9, "Rhetorical Questions", "Rhetorical Guiding", "Why burn money on blind ads when server tracking fixes it?", "উত্তর না চেয়ে নিজের পয়েন্টের গুরুত্ব বোঝানো।", "Say: Who wouldn't want 25% more tracked sales?"),
    (174, 9, "Expressing Genuine Surprise", "Get out of here!", "Get out of here! The client approved the contract in 10 minutes?", "খাঁটি বিস্ময় প্রকাশ।", "Say: No kidding! That's awesome."),
    (175, 9, "Active Listening Interjections", "Uh-huh / Gotcha / Right", "Uh-huh... right... absolutely makes sense.", "কথা শোনার সময় সায় দিয়ে এক্টিভ লিসেনিং বজায় রাখা।", "Say: Right, gotcha, totally agree."),
    (176, 9, "Cooperative Sentence Completion", "Finishing Sentences", "...and that's when the conversion value matches 100%.", "অন্যের কথার শেষাংশ ধরে সুন্দরভাবে সম্পূরক কথা বলা।", "Say: Exactly, right on the money."),
    (177, 9, "Graceful Call Wrap-Up", "Respecting Time", "I want to be respectful of your time, so let's wrap up here.", "ভদ্রভাবে ক্লায়েন্টের সময় বাঁচিয়ে কল শেষ করা।", "Say: I know you have another call, so let's pause here."),
    (178, 9, "Spoken Asymmetry", "Prompting Buyer Inquiries", "There are two ways to fix this—one takes 2 hours, one is permanent.", "সংক্ষিপ্ত কথা বলে বায়ারকে প্রশ্ন করতে বাধ্য করা।", "Say: Which approach do you prefer?"),
    (179, 9, "Confidence Micro-Affirmations", "Absolutely / Consider it done", "Consider it done. I'll have the QA report over by 3 PM.", "কাজের দায়িত্ব নিয়ে দৃঢ় নিশ্চয়তা দেওয়া।", "Say: Absolutely, consider it done."),
    (180, 9, "Casual Voice-Note Signoffs", "Catch you on the flip side", "Talk soon! Catch you on the flip side.", "বন্ধুসুলভ ও আধুনিক বিদায় নেওয়া।", "Say: Catch you later, take care!"),

    # Module 10: Elite Pronunciation, Rhythm & 180-WPM Speed Drills (181-200)
    (181, 10, "American Flap-T Speed Loops", "Flap-T Speed Loop", "A better bottle of water is waiting at the city center.", "দ্রুত নরম D এর মতো T উচ্চারণ প্র্যাকটিস।", "Repeat 5 times fast: Water bottle, better butter."),
    (182, 10, "Glottal Stop Speed Chains", "Glottal Stop Chain", "The certain button on the mountain was written in Latin.", "গলা আটকে T না ছাড়ার দ্রুত ড্রিল।", "Say: Certain button, written mountain."),
    (183, 10, "The Dark-L vs Light-L Agility", "Dark-L Agility", "Will you fill the real container till the bell rings?", "জিহ্বার পেছনের অংশ উঁচিয়ে ডার্ক-এল প্র্যাকটিস।", "Say: Real thrill, fill the bill."),
    (184, 10, "Complex Consonant Clusters (-sks, -sts)", "Consonant Clusters", "He tests six tasks and asks for new requests.", "শব্দের শেষে কঠিন কনসোনেন্ট জোড়া না ফেলে পরিষ্কার বলা।", "Say: Tasks, tests, asks, requests, lists."),
    (185, 10, "Vocal Fry & Low Chest Resonance", "Chest Resonance", "Good morning team, let's look at the analytics report.", "বুকের গভীর থেকে রিল্যাক্সড ও ভারী আমেরিকান টোন আনা।", "Take a deep breath and speak from the lower chest."),
    (186, 10, "Intonation Melody (Jump Up, Step Down)", "Intonation Wave", "I checked the container, and everything is working properly.", "নতুন তথ্যে ভয়েস উপরে ওঠা এবং বাক্য শেষে নামা।", "Follow the melodic wave: Up on 'container', down on 'properly'."),
    (187, 10, "Content Word Stress vs Grammar Compression", "Rhythm Compression", "We DEPLOYED the TAGS on the SERVER CONTAINER.", "মূল শব্দে জোর দেওয়া এবং ব্যাকরণ শব্দ সংকুচিত করা।", "Clap on the capitalized words only."),
    (188, 10, "Thought Group Breath Timing", "Thought Groups", "When the pixel fires, [breath] Meta receives the hash [breath].", "বাক্যের স্বাভাবিক বিরতিতে সঠিক শ্বাস নেওয়া।", "Breathe only at natural punctuation breaks."),
    (189, 10, "Tongue Agility Twisters", "Tongue Twister", "Red lorry, yellow lorry, unique New York.", "জিহ্বার জড়তা কাটিয়ে গতি বাড়ানোর সুপার ড্রিল।", "Say 3 times as fast as possible."),
    (190, 10, "180-WPM Native Shadowing Protocol", "Native Shadowing", "Follow the native speaker's audio like an echo half a second behind.", "নেটিভ মানুষের কথার ঠিক ০.৫ সেকেন্ড পেছনে থেকে মুখে বলা।", "Shadow the bot's voice audio note in real time."),
    (191, 10, "Lip Position Switching (/w/ to /v/)", "W to V Switch", "Very well, William viewed the video with Walter.", "ঠোঁট গোল করা থেকে দাঁতে ছোঁয়ানোর বিদ্যুৎগতির সুইচ।", "Say: Very well, William viewed."),
    (192, 10, "Eliminating Dental Stops", "Alveolar T/D", "Today the data director delivered ten deliverables.", "দাঁতের পেছনে মাড়ির ওপরে জিহ্বা রেখে T/D বলা।", "Tap the alveolar ridge behind your teeth."),
    (193, 10, "Perfecting American Retroflex /r/ Curl", "Retroflex R", "Rarely are there rare records reported right.", "জিহ্বা উল্টে তালুর দিকে কার্ল করে আমেরিকান R বলা।", "Curl the tongue back without touching the roof."),
    (194, 10, "Vowel Lengthening Before Voiced Consonants", "Vowel Lengthening", "The bad bat had a sad sat in the red bed.", "ভয়েসড কনসোনেন্টের আগের ভাওয়েল দীর্ঘ করা।", "Hold the vowel longer in 'bad' than 'bat'."),
    (195, 10, "Fast Contractive Questioning", "Didn't you? / Haven't you?", "You saw the GTM tag, didn't you?", "দ্রুত সংকুচিত প্রশ্ন ছুড়ে দেওয়া।", "Say: Didn't you? Wouldn't you? Couldn't you?"),
    (196, 10, "Rapid Tag Questions", "Isn't it? / Won't they?", "The attribution looks clean, doesn't it?", "বাক্যের শেষে দ্রুত কনফার্মেশন প্রশ্ন জুড়ে দেওয়া।", "Say: Isn't it? Doesn't it? Won't they?"),
    (197, 10, "Rhythm Clapping & Metronome Speaking", "Metronome Rhythm", "ONE and TWO and THREE and FOUR, TRACK the DATA on the FLOOR.", "মেট্রোনোমের তালের সাথে ইংরেজি বলা।", "Clap hands to keep a strict 120-BPM beat."),
    (198, 10, "Overcoming Speaking Anxiety (Vagus Nerve)", "Vagus Reset", "Exhale slowly through the mouth before unmuting on Zoom.", "কথা বলার আগে বুক ফুলিয়ে শ্বাস নিয়ে নার্ভ শান্ত করা।", "Take 1 long exhale before you speak on calls."),
    (199, 10, "Instant On-The-Fly Self-Correction", "Smooth Self-Recovery", "...or rather, what I meant to say was the server payload.", "ভুল হলে লজ্জা না পেয়ে মসৃণভাবে সংশোধন করা।", "Say: ...or rather, what I mean is..."),
    (200, 10, "The Fluid English Mental Monologue", "Thinking in English 24/7", "Describe everything you see and do in English inside your head.", "বাংলা থেকে অনুবাদ না করে মনে মনে সবসময় ইংরেজিতে ভাবা।", "Narrate your day inside your mind in fast English.")
]

def get_skill(number: int):
    """Retrieve a single skill by number (1 to 200)."""
    if 1 <= number <= len(SKILLS):
        item = SKILLS[number - 1]
        return {
            "number": item[0],
            "module_id": item[1],
            "module_name": MODULES.get(item[1], ""),
            "title": item[2],
            "formula": item[3],
            "example": item[4],
            "bangla": item[5],
            "drill": item[6]
        }
    return None

def search_skills(query: str, limit: int = 5):
    """Search skills by keyword in title, formula, example or bangla explanation."""
    q = query.lower()
    results = []
    for item in SKILLS:
        if q in item[2].lower() or q in item[3].lower() or q in item[4].lower() or q in item[5].lower():
            results.append({
                "number": item[0],
                "module_id": item[1],
                "module_name": MODULES.get(item[1], ""),
                "title": item[2],
                "formula": item[3],
                "example": item[4],
                "bangla": item[5],
                "drill": item[6]
            })
            if len(results) >= limit:
                break
    return results

def get_module_skills(module_id: int):
    """Get all 20 skills in a module."""
    results = []
    for item in SKILLS:
        if item[1] == module_id:
            results.append({
                "number": item[0],
                "title": item[2],
                "formula": item[3],
                "example": item[4],
                "bangla": item[5],
                "drill": item[6]
            })
    return results
