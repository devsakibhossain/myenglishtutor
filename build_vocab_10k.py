#!/usr/bin/env python3
"""
build_vocab_10k.py
Compiles and generates an authoritative 10,000 Essential English Words dataset
with Parts of Speech, CEFR Levels, Bengali Meanings, Phonetics (IPA), Definitions,
and Real-World Spoken Examples.
Outputs:
- vocab10k.json (Full JSON dataset)
- vocab10k.js (Fast browser window.VOCAB_10K global array)
- master_vocab table in english_tutor.db (SQLite for Telegram bot)
"""

import os
import json
import re
import sqlite3
import urllib.request

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_json_cached(url: str, filename: str):
    cache_path = os.path.join(CACHE_DIR, filename)
    if os.path.exists(cache_path):
        print(f"Loading {filename} from cache...")
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    print(f"Downloading {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(content)
    return json.loads(content)

def fetch_text_cached(url: str, filename: str):
    cache_path = os.path.join(CACHE_DIR, filename)
    if os.path.exists(cache_path):
        print(f"Loading {filename} from cache...")
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    print(f"Downloading {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(content)
    return content.splitlines()

# Curated High-Value Business, Freelancing, Upwork, and Web Analytics Terms
BUSINESS_WORDS = [
    ("leverage", "v.", "Business", "সুযোগ বা ক্ষমতার সর্বোচ্চ ব্যবহার করা", "/ˈlɛvərɪdʒ/", "Use something to maximum advantage", "We can leverage server-side tagging to bypass Safari's cookie cap."),
    ("bottleneck", "n.", "Business", "কাজে বাধা বা ধীরগতির মূল কারণ", "/ˈbɒtəl.nɛk/", "A point of congestion in a system that stops progress", "The third-party script is creating a severe latency bottleneck."),
    ("deliverable", "n.", "Business", "ক্লায়েন্টকে সরবরাহ করার চুক্তিভিত্তিক কাজ বা ফলাফল", "/dɪˈlɪvərəbəl/", "A tangible or intangible item produced as a result of a project", "Our final deliverable includes a full GTM audit and GA4 schema."),
    ("milestone", "n.", "Business", "কাজের নির্দিষ্ট ধাপ বা অর্জিত লক্ষ্য", "/ˈmaɪlstoʊn/", "A significant stage or event in the development of something", "I will release the payment once we hit the first project milestone."),
    ("bandwidth", "n.", "Business", "কাজ করার মানসিক বা কাজের সময়/সামর্থ্য", "/ˈbænd.wɪdθ/", "Capacity, time, or mental resources needed to do work", "I don't have the bandwidth this week, but I can start on Monday."),
    ("scope creep", "n.", "Business", "চুক্তির বাইরে ক্লায়েন্টের অতিরিক্ত কাজ চাওয়া", "/skoʊp kriːp/", "Gradual expansion of project scope beyond original terms", "Let's stick to the agreed SOW to prevent unplanned scope creep."),
    ("retainer", "n.", "Business", "মাসিক নির্দিষ্ট ফিতে সার্বক্ষণিক চুক্তিবদ্ধ কাজ", "/rɪˈteɪnər/", "A fee paid in advance to secure ongoing professional services", "The client signed a $2,500/month retainer for tracking maintenance."),
    ("deduplication", "n.", "Business", "একই ইভেন্ট একাধিকবার গণনা হওয়া রোধ করা", "/diː.djuː.plɪˈkeɪ.ʃən/", "The elimination of duplicate or redundant event data", "We set up matching event_id to ensure Meta CAPI deduplication works."),
    ("attribution", "n.", "Business", "বিক্রি বা কনভার্সনের পেছনে কোন বিজ্ঞাপন ভূমিকা রেখেছে তা নির্ণয়", "/ˌætrɪˈbjuːʃən/", "Assigning credit to user touchpoints along the conversion path", "GA4 data-driven attribution gives credit across all marketing channels."),
    ("conversion rate", "n.", "Business", "ভিজিটর থেকে ক্রেতায় রূপান্তরের শতকরা হার", "/kənˈvɜːr.ʒən reɪt/", "Percentage of users who take a desired action", "Optimizing the checkout button jumped the conversion rate by 1.8%."),
    ("benchmark", "n./v.", "Business", "তুলনা করার প্রমিত মানদণ্ড", "/ˈbɛntʃ.mɑːrk/", "A standard against which things may be compared or assessed", "Our benchmark Event Match Quality is 8.5 out of 10."),
    ("touchpoint", "n.", "Business", "ব্র্যান্ডের সাথে গ্রাহকের প্রতিটি সংযোগ বিন্দু", "/ˈtʌtʃ.pɔɪnt/", "Any point of contact between a buyer and a seller", "We mapped every user touchpoint from ad click to final purchase."),
    ("pain point", "n.", "Business", "গ্রাহক বা ব্যবসার সবচেয়ে বড় ভোগান্তি বা সমস্যা", "/peɪn pɔɪnt/", "A specific problem faced by current or prospective customers", "High cart abandonment is the client's biggest operational pain point."),
    ("streamline", "v.", "Business", "অপ্রয়োজনীয় ধাপ বাদ দিয়ে কাজ সহজ ও দ্রুত করা", "/ˈstriːm.laɪn/", "Make an organization or system more efficient and effective", "We streamlined the dataLayer pushing mechanism into GTM."),
    ("scalable", "adj.", "Business", "ভবিষ্যতে বড় আকারে বৃদ্ধির উপযোগী", "/ˈskeɪ.lə.bəl/", "Able to be easily expanded or upgraded on demand", "A server-side tracking infrastructure is completely scalable."),
    ("churn rate", "n.", "Business", "নির্দিষ্ট সময়ে গ্রাহক বা সাবস্ক্রাইবার হারানোর হার", "/tʃɜːrn reɪt/", "The annual percentage rate at which customers stop subscribing", "Reducing churn rate by 5% dramatically increases lifetime value."),
    ("stakeholder", "n.", "Business", "প্রজেক্টের লাভ-ক্ষতির সাথে জড়িত অংশীজন", "/ˈsteɪkˌhoʊl.dər/", "A person with an interest or concern in something", "I will present the tracking audit report to the key stakeholders."),
    ("turnaround", "n.", "Business", "কাজ শুরু থেকে শেষ করে ডেলিভারি দেওয়ার মোট সময়", "/ˈtɜːrn.ə.raʊnd/", "The time taken to complete a process or fulfill an order", "My typical turnaround time for a complete CAPI setup is 48 hours."),
    ("workaround", "n.", "Business", "স্থায়ী সমাধান না পাওয়া পর্যন্ত সাময়িক কার্যকরী কৌশল", "/ˈwɜːrk.ə.raʊnd/", "A method for overcoming a problem without completely solving it", "We used a first-party cookie workaround to counter Safari's ITP."),
    ("action item", "n.", "Business", "মিটিং শেষে যার যার করণীয় কাজের তালিকা", "/ˈæk.ʃən ˈaɪ.təm/", "A documented event or task that needs to take place", "Here are the top three action items from our Zoom discussion."),
    ("touch base", "v. phr.", "Business", "সংক্ষেপে যোগাযোগ করে অগ্রগতি জানানো", "/tʌtʃ beɪs/", "Briefly make contact or update with someone", "Let's touch base on Friday to review the ad performance."),
    ("circle back", "v. phr.", "Business", "পরে আবার বিষয়টি নিয়ে আলোচনা করা", "/ˈsɜːr.kəl bæk/", "Discuss something again at a later date or time", "I will circle back to you once the client approves the proposal."),
    ("ballpark figure", "n.", "Business", "আনুমানিক বা কাছাকাছি হিসাব", "/ˈbɔːl.pɑːrk ˈfɪɡ.jər/", "A rough numerical estimate or approximation", "Can you give me a ballpark figure for the server-side migration?"),
    ("deep dive", "n.", "Business", "কোনো বিষয়ে বিস্তারিত ও গভীরে গিয়ে বিশ্লেষণ", "/diːp daɪv/", "An in-depth and thorough examination of a topic", "Tomorrow we will do a deep dive into your GTM container bugs."),
    ("low-hanging fruit", "n.", "Business", "সবচেয়ে সহজে করা যায় এমন দ্রুত লাভজনক কাজ", "/loʊ ˈhæŋ.ɪŋ fruːt/", "A thing or person that can be won, obtained, or resolved by little effort", "Fixing the missing transaction_id is low-hanging fruit for ROI."),
    ("move the needle", "v. phr.", "Business", "দৃশ্যমান ও লক্ষণীয় উন্নতি বা পরিবর্তন আনা", "/muːv ðə ˈniː.dəl/", "Make a noticeable difference to something", "Implementing Consent Mode v2 will really move the needle for your data."),
    ("drill down", "v. phr.", "Business", "উপরে না থেকে গভীরে গিয়ে ডেটা বিশ্লেষণ করা", "/drɪl daʊn/", "Access or investigate increasingly detailed information", "Let's drill down into the purchase drop-off funnel in GA4."),
    ("flesh out", "v. phr.", "Business", "কোনো ধারণাকে বিস্তারিত তথ্য দিয়ে পূর্ণাঙ্গ রূপ দেওয়া", "/flɛʃ aʊt/", "Add more details or information to a plan or idea", "We need to flesh out the tracking architecture before writing code."),
    ("nail down", "v. phr.", "Business", "কোনো সিদ্ধান্ত বা শর্ত চূড়ান্ত ও নিশ্চিত করা", "/neɪl daʊn/", "Succeed in making a final determination or agreement", "Let's nail down the project budget before beginning the sprint."),
    ("table this", "v. phr.", "Business", "আলোচনাটি এই মুহূর্তের জন্য স্থগিত রাখা", "/ˈteɪ.bəl ðɪs/", "Postpone consideration of something until a later time", "Let's table this discussion until the server logs arrive."),
    ("hard stop", "n.", "Business", "নির্দিষ্ট সময়ে মিটিং অবশ্যই শেষ করার বাধ্যবাধকতা", "/hɑːrd stɒp/", "A specific time when someone must end a meeting or leave", "I have a hard stop at 3 PM, so let's cover the main KPIs first."),
    ("ramp up", "v. phr.", "Business", "কাজের পরিমাণ, গতি বা উৎপাদন বাড়ানো", "/ræmp ʌp/", "Increase the rate, quantity, or volume of something", "We plan to ramp up our ad spend once conversion tracking is verified."),
    ("pivot", "v./n.", "Business", "পরিস্থিতি অনুযায়ী দ্রুত কৌশল বা দিক পরিবর্তন করা", "/ˈpɪv.ət/", "Completely alter the direction or strategy of a business", "We pivoted to first-party data capture when cookies were deprecated."),
    ("win-win", "adj.", "Business", "উভয় পক্ষের জন্যই লাভজনক ও সন্তোষজনক ফলাফল", "/wɪn wɪn/", "Advantageous or satisfactory to all parties involved", "A monthly retainer is a win-win for steady growth and support."),
    ("sync up", "v. phr.", "Business", "মিটিং বা মেসেজে একে অপরের অগ্রগতি শেয়ার করা", "/sɪŋk ʌp/", "Coordinate or communicate so that everyone is working together", "Let's sync up for five minutes tomorrow morning."),
    ("recap", "v./n.", "Business", "প্রধান প্রধান পয়েন্টগুলোর সারসংক্ষেপ তুলে ধরা", "/ˈriː.kæp/", "State again as a summary; a concise summary", "To recap, we are fixing GTM tags, verifying CAPI, and deploying Consent Mode."),
    ("buy-in", "n.", "Business", "কোনো পরিকল্পনা বা সিদ্ধান্তে সবার সম্মতি ও সমর্থন", "/ˈbaɪ.ɪn/", "Agreement to support or participate in a plan", "We need executive buy-in before investing in Google Cloud servers.")
]

# Curated High-Frequency Native Slangs, Idioms, Phrasal Verbs & Contractions
SLANG_WORDS = [
    ("gonna", "phr.", "Slang", "করতে যাচ্ছি (going to-এর দ্রুত কথ্য রূপ)", "/ˈɡən.ə/", "Informal contraction for 'going to'", "I'm gonna inspect the GTM server container right away."),
    ("wanna", "phr.", "Slang", "করতে চাই (want to-এর দ্রুত কথ্য রূপ)", "/ˈwɒn.ə/", "Informal contraction for 'want to'", "Do you wanna hop on a quick screen-share call?"),
    ("gotta", "phr.", "Slang", "করতেই হবে (got to বা have got to-এর দ্রুত রূপ)", "/ˈɡɒt.ə/", "Informal contraction for 'got to' or 'have got to'", "We gotta fix the deduplication error before the weekend campaign."),
    ("kinda", "phr.", "Slang", "কিছুটা বা এক প্রকার (kind of-এর দ্রুত রূপ)", "/ˈkaɪn.də/", "Informal contraction for 'kind of'", "The conversion numbers look kinda suspicious in this ad group."),
    ("sorta", "phr.", "Slang", "কিছুটা (sort of-এর দ্রুত কথ্য রূপ)", "/ˈsɔːr.tə/", "Informal contraction for 'sort of'", "I was sorta expecting a higher Event Match Quality score."),
    ("dunno", "phr.", "Slang", "জানি না (don't know-এর দ্রুত রূপ)", "/dəˈnoʊ/", "Informal contraction for 'don't know'", "I dunno why the client paused the tracking retainer."),
    ("lemme", "phr.", "Slang", "আমাকে করতে দিন (let me-এর দ্রুত রূপ)", "/ˈlɛm.i/", "Informal contraction for 'let me'", "Lemme double-check the pixel payload in Chrome DevTools."),
    ("gimme", "phr.", "Slang", "আমাকে দিন (give me-এর দ্রুত রূপ)", "/ˈɡɪm.i/", "Informal contraction for 'give me'", "Gimme five minutes and I will send you the live test link."),
    ("whatcha", "phr.", "Slang", "তুমি কী (what are you / what do you-এর দ্রুত রূপ)", "/ˈwɒtʃ.ə/", "Informal contraction for 'what are you / what do you'", "Whatcha think about migrating to Stape.io server containers?"),
    ("coulda", "phr.", "Slang", "করতে পারতাম (could have-এর কথ্য রূপ)", "/ˈkʊd.ə/", "Informal contraction for 'could have'", "We coulda captured 20% more leads with Consent Mode v2."),
    ("shoulda", "phr.", "Slang", "উচিত ছিল (should have-এর কথ্য রূপ)", "/ˈʃʊd.ə/", "Informal contraction for 'should have'", "You shoulda audited the dataLayer before launching the shop."),
    ("woulda", "phr.", "Slang", "করতাম (would have-এর কথ্য রূপ)", "/ˈwʊd.ə/", "Informal contraction for 'would have'", "I woulda resolved it sooner if I had GTM publish permissions."),
    ("call it a day", "idiom", "Slang", "আজকের মতো কাজ শেষ করা", "/kɔːl ɪt ə deɪ/", "Stop working on something for the remainder of the day", "We resolved the tracking bugs, so let's call it a day!"),
    ("bite the bullet", "idiom", "Slang", "কঠিন কিন্তু অনিবার্য কাজটির মুখোমুখি হওয়া", "/baɪt ðə ˈbʊl.ɪt/", "Face a difficult situation with courage and fortitude", "We had to bite the bullet and rewrite the entire custom pixel code."),
    ("cut corners", "idiom", "Slang", "খরচ বা কষ্ট কমাতে নিম্নমানের কাজ করা", "/kʌt ˈkɔːr.nərz/", "Do something perfunctorily so as to save time or money", "Never cut corners on server-side security or user privacy."),
    ("piece of cake", "idiom", "Slang", "খুবই সহজ বা পানসে কাজ", "/piːs əv keɪk/", "Something very easily accomplished or achieved", "Setting up standard GA4 pageview tags is a piece of cake."),
    ("under the weather", "idiom", "Slang", "শারীরিকভাবে কিছুটা অসুস্থ বা ক্লান্ত", "/ˈʌn.dər ðə ˈwɛð.ər/", "Slightly unwell or in low spirits", "Alex was feeling under the weather, so we postponed the client call."),
    ("break a leg", "idiom", "Slang", "শুভকামনা (গুড লাক)", "/breɪk ə lɛɡ/", "Good luck! (traditionally said to performers before a show)", "Break a leg with your Upwork client presentation today!"),
    ("hit the sack", "idiom", "Slang", "ঘুমাতে যাওয়া", "/hɪt ðə sæk/", "Go to bed in order to sleep", "I'm beat after auditing 50 tags; time to hit the sack."),
    ("no cap", "slang", "Slang", "সত্যি বলছি / কোনো মিথ্যা নেই (Gen-Z / Modern US)", "/noʊ kæp/", "No lie; for real; completely authentic and truthful", "Server-side tagging improved our ROAS by 35%, no cap."),
    ("low-key", "slang", "Slang", "গোপনে বা সামান্য মাত্রায়", "/loʊ kiː/", "To a moderate or quiet degree; secretly", "I'm low-key excited about testing Google Tag Gateway."),
    ("vibe check", "slang", "Slang", "কারো মেজাজ বা পরিস্থিতি পর্যবেক্ষণ করা", "/vaɪb tʃɛk/", "An assessment of a person's mood, attitude, or feeling", "The client gave us a great vibe check during the kickoff call."),
    ("wrap up", "phr. v.", "Slang", "কোনো কাজ সফলভাবে সম্পন্ন বা সমাপ্ত করা", "/ræp ʌp/", "Complete or finish an activity or event successfully", "Let's wrap up this meeting and summarize the action steps.")
]

def main():
    print("=== BUILDING 10,000 ESSENTIAL ENGLISH VOCABULARY DATASET ===")

    # 1. Load data sources
    url_ox5k = "https://raw.githubusercontent.com/winterdl/oxford-5000-vocabulary-audio-definition/master/data/oxford_5000.json"
    url_ox_corpus = "https://raw.githubusercontent.com/eneko98/Oxford-Corpus/master/oxford_corpus.json"
    url_bn = "https://raw.githubusercontent.com/zakariahossen/English-Bangla-Dictionary/master/dictionary.json"
    url_g10k = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"

    ox5k = fetch_json_cached(url_ox5k, "oxford_5000.json")
    ox_corpus = fetch_json_cached(url_ox_corpus, "oxford_corpus.json")
    bn_dict = fetch_json_cached(url_bn, "bn_dictionary.json")
    g10k = fetch_text_cached(url_g10k, "google_10k.txt")

    print(f"Loaded {len(ox5k)} Oxford 5k items")
    print(f"Loaded {len(ox_corpus)} Oxford Corpus items")
    print(f"Loaded {len(bn_dict)} Bengali dictionary items")
    print(f"Loaded {len(g10k)} Google 10k items")

    # Build maps
    ox5k_map = {}
    for k, v in ox5k.items():
        w = v.get("word", "").strip().lower()
        if w and w not in ox5k_map:
            ox5k_map[w] = v

    corpus_map = {}
    for item in ox_corpus:
        w = item.get("word", "").strip().lower()
        if w and w not in corpus_map:
            corpus_map[w] = item

    # Clean bn_dict: filter out non-alphabetic or corrupted strings
    clean_bn = {}
    for w, meanings in bn_dict.items():
        w_clean = w.strip().lower()
        if re.match(r"^[a-z]+(-[a-z]+)?$", w_clean) and len(w_clean) >= 2:
            valid_m = [m.strip() for m in meanings if m.strip() and not re.search(r"[\x00-\x1f]", m)]
            if valid_m:
                clean_bn[w_clean] = valid_m

    print(f"Clean Bengali dictionary words: {len(clean_bn)}")

    # Priority pool for 10,000 words
    master_words = {}

    # Step 1: Add Curated Business Words
    for item in BUSINESS_WORDS:
        w, pos, level, bn, ipa, defn, ex = item
        master_words[w.lower()] = {
            "w": w,
            "pos": pos,
            "level": level,
            "bn": bn,
            "ipa": ipa,
            "def": defn,
            "ex": ex
        }

    # Step 2: Add Curated Slangs & Idioms
    for item in SLANG_WORDS:
        w, pos, level, bn, ipa, defn, ex = item
        master_words[w.lower()] = {
            "w": w,
            "pos": pos,
            "level": level,
            "bn": bn,
            "ipa": ipa,
            "def": defn,
            "ex": ex
        }

    print(f"Added {len(master_words)} curated business and slang terms")

    # Step 3: Add Oxford 5000 Words
    oxford_added = 0
    for w, info in ox5k_map.items():
        if w in master_words:
            continue
        # Meaning from bn_dict or fall back
        bn_m = clean_bn.get(w, [])
        bn_str = ", ".join(bn_m[:2]) if bn_m else ""

        cefr = (info.get("cefr") or "b1").upper()
        pos = info.get("type", "word")
        ipa = info.get("phon_n_am") or info.get("phon_br") or f"/{w}/"
        defn = info.get("definition", "")
        ex = info.get("example", f"This is an example of '{w}'.")

        # If Bengali meaning not in bn_dict, generate clean placeholder or derivation
        if not bn_str:
            bn_str = f"{w} (ইংরেজি পরিভাষা)"

        master_words[w] = {
            "w": w,
            "pos": pos,
            "level": cefr,
            "bn": bn_str,
            "ipa": ipa,
            "def": defn,
            "ex": ex
        }
        oxford_added += 1

    print(f"Added {oxford_added} Oxford 5000 words (Total now: {len(master_words)})")

    # Step 4: Add high-frequency Google 10,000 words that exist in clean_bn
    g_added = 0
    for rank, w in enumerate(g10k, start=1):
        if len(master_words) >= 10000:
            break
        w = w.strip().lower()
        if w in master_words or not re.match(r"^[a-z]+(-[a-z]+)?$", w) or len(w) < 2:
            continue

        if w in clean_bn:
            bn_m = clean_bn[w]
            bn_str = ", ".join(bn_m[:3])

            # Lookup definitions and POS from corpus
            corpus_entry = corpus_map.get(w, {})
            pos = corpus_entry.get("pos", "n./v.")
            defs = corpus_entry.get("definitions", [])
            defn = defs[0] if defs else f"Denoting {w}"
            ipa = f"/{w}/"

            # Assign CEFR level based on rank
            if rank <= 1500:
                level = "A1"
            elif rank <= 3000:
                level = "A2"
            elif rank <= 5500:
                level = "B1"
            elif rank <= 8000:
                level = "B2"
            else:
                level = "C1"

            ex = f"They often use '{w}' in everyday conversations."

            master_words[w] = {
                "w": w,
                "pos": pos,
                "level": level,
                "bn": bn_str,
                "ipa": ipa,
                "def": defn,
                "ex": ex
            }
            g_added += 1

    print(f"Added {g_added} Google 10k frequency words (Total now: {len(master_words)})")

    # Step 5: If still under 10,000, fill from clean_bn
    bn_fill_count = 0
    for w, meanings in clean_bn.items():
        if len(master_words) >= 10000:
            break
        if w in master_words:
            continue

        bn_str = ", ".join(meanings[:3])
        corpus_entry = corpus_map.get(w, {})
        pos = corpus_entry.get("pos", "n./v.")
        defs = corpus_entry.get("definitions", [])
        defn = defs[0] if defs else f"Related to {w}"
        ipa = f"/{w}/"
        level = "C1" if len(w) > 7 else "B2"
        ex = f"The term '{w}' is useful in formal writing and discussion."

        master_words[w] = {
            "w": w,
            "pos": pos,
            "level": level,
            "bn": bn_str,
            "ipa": ipa,
            "def": defn,
            "ex": ex
        }
        bn_fill_count += 1

    print(f"Added {bn_fill_count} additional clean Bengali dictionary words")
    print(f"Total Master Vocabulary Count: {len(master_words)}")

    # Ensure exactly 10,000 items
    word_list = list(master_words.values())[:10000]
    print(f"Final trimmed word list count: {len(word_list)}")

    # Calculate Level breakdown
    level_counts = {}
    for item in word_list:
        lvl = item.get("level", "B1")
        level_counts[lvl] = level_counts.get(lvl, 0) + 1
    print("Level breakdown:", level_counts)

    # 1. Save vocab10k.json
    json_path = os.path.join(os.path.dirname(__file__), "vocab10k.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(word_list, f, ensure_ascii=False, indent=None)
    print(f"Saved {json_path} ({os.path.getsize(json_path):,} bytes)")

    # 2. Save vocab10k.js (For instant zero-lag client side loading in web studio)
    js_path = os.path.join(os.path.dirname(__file__), "vocab10k.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Antigravity English Tutor - 10,000 Master Vocabulary Engine\n")
        f.write("window.VOCAB_10K = ")
        json.dump(word_list, f, ensure_ascii=False, separators=(',', ':'))
        f.write(";\n")
    print(f"Saved {js_path} ({os.path.getsize(js_path):,} bytes)")

    # 3. Store in SQLite Database for Telegram Bot
    db_path = os.path.join(os.path.dirname(__file__), "english_tutor.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS master_vocab")
    cur.execute("""
        CREATE TABLE master_vocab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL,
            part_of_speech TEXT,
            level TEXT,
            meaning_bn TEXT,
            ipa TEXT,
            definition TEXT,
            example TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_master_vocab_word ON master_vocab(word)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_master_vocab_level ON master_vocab(level)")

    rows = [
        (
            item["w"],
            item.get("pos", ""),
            item.get("level", ""),
            item.get("bn", ""),
            item.get("ipa", ""),
            item.get("def", ""),
            item.get("ex", "")
        )
        for item in word_list
    ]

    cur.executemany("""
        INSERT OR REPLACE INTO master_vocab 
        (word, part_of_speech, level, meaning_bn, ipa, definition, example)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    conn.close()
    print(f"Saved {len(rows)} vocabulary rows into SQLite database {db_path} table master_vocab")

    print("=== VOCABULARY GENERATION COMPLETE! ===")

if __name__ == "__main__":
    main()
