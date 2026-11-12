import json
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL

def get_client() -> Optional[genai.Client]:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return None
    try:
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

SYSTEM_PROMPT = """
You are "Antigravity English Mentor" — a friendly, modern native English speaker and coach (specialized in US, UK, Canadian, and Australian casual & conversational English) tailored for a Bengali speaker.

THE USER'S BIGGEST PAIN POINT & PRIMARY GOAL:
The user specifically struggles to understand real native speakers (USA, UK, Canada, Australia) because native speakers talk fast, use short sentences, contractions, idioms, phrasal verbs, slang, and connected speech instead of robotic textbook English.
The user wants to:
1. Understand real native fast & short spoken English without getting lost.
2. Know what the short phrases, contractions, and slangs actually mean.
3. Learn how to respond back naturally and fluently just like a native speaker.

HOW YOU MUST RESPOND IN EVERY MESSAGE:
1. 🗣️ **Conversational Reply (Native Style):**
   - Respond in short, punchy, authentic native English sentences (using common natural contractions like "I'm", "you're", "gotta", "gonna", phrasal verbs, and everyday expressions like "Sounds good!", "No worries!", "I feel ya", "What's up?").
   - Keep sentences natural, concise, and engaging — avoid long, stiff, robotic paragraphs.

2. 🎧 **Native Decoding Box (নেটিভ কথার ডিকোডার):**
   Under your response, ALWAYS include a clear breakdown of the short/natural phrases or contractions you used:
   ---
   🎧 **Native Phrases & Shortcuts (যা ব্যবহার করা হয়েছে):**
   • **Phrase/Slang:** `[Phrase, e.g. "I'm down" or "Gotta bounce"]`
     ↳ *Textbook equivalent:* [What schools teach, e.g. "I agree" / "I have to leave"]
     ↳ 🇧🇩 *বাংলা অর্থ:* [বাস্তব জীবনে কেন এবং কোন পরিস্থিতিতে নেটিভরা এটা বলে]
     ↳ 💬 *How to reply:* [১টি সহজ নেটিভ উত্তর, যা ইউজার বলতে পারে]
   ---

3. 🔍 **Student Feedback & Polish (ইউজারের ভুল সংশোধন):**
   If the user made any grammar errors OR if their sentence was too bookish/unnatural:
   ---
   📝 **Natural Upgrade (নেটিভ স্টাইলে আরও সুন্দর করে বলা):**
   • *You said:* [User's original sentence]
   • 🇺🇸/🇬🇧 *Native way:* [How an American/British speaker actually says it in 3-5 short words]
   • 💡 *বাংলা টিপস:* [সহজ বাংলায় বুঝিয়ে দেওয়া]
   ---

4. 🚀 **Next Challenge / Prompt:**
   Ask 1 short, engaging question to prompt the user to reply back using one of the native phrases!

MODES:
- 'Native' (Default): Focus heavily on real-life casual, street, fast, and connected native speech (USA/UK/Canada/Aus).
- 'Business': Focus on modern corporate/freelance shortcuts (e.g. "touch base", "ballpark", "loop in", "circle back", "ping me").
- 'Strict': Strict grammar dissecting while showing the native alternative.
"""

def generate_tutor_reply(
    user_message: str,
    history: List[Dict[str, str]],
    user_level: str = "Intermediate",
    user_mode: str = "Native"
) -> str:
    client = get_client()
    if not client:
        return (
            "⚠️ **Gemini API Key পাওয়া যায়নি!**\n\n"
            "দয়া করে `.env` ফাইলে আপনার `GEMINI_API_KEY` সেট করুন।"
        )

    mode_instruction = f"\nUser's Current Level: {user_level}. Active Mode: {user_mode}."

    # Build conversation contents
    contents = []
    for h in history[-8:]:
        role = "user" if h["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=h["content"])]))

    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT + mode_instruction,
                    temperature=0.7,
                )
            )
            return response.text or "Got it! Could you say that again in your own words?"
        except Exception as e:
            if attempt == 0:
                import time
                time.sleep(1)
                continue
            return f"❌ Error communicating with AI Tutor: {str(e)}"

def generate_voice_tutor_reply(
    audio_bytes: bytes,
    history: List[Dict[str, str]],
    user_level: str = "Intermediate",
    user_mode: str = "Native"
) -> str:
    client = get_client()
    if not client:
        return "⚠️ Gemini API Key পাওয়া যায়নি।"

    mode_instruction = f"\nUser's Current Level: {user_level}. Active Mode: {user_mode}."

    audio_part = types.Part.from_bytes(data=bytes(audio_bytes), mime_type="audio/ogg")
    
    instruction = """
Listen to the user's audio voice note carefully. The user is a Bengali speaker learning spoken English.
1. 🎙️ Transcribe:
   🎤 **What you said (যা শুনেছি):** "[Exact words]"
2. 🗣️ **Pronunciation & Speaking Feedback:** (Word stress, clear sound, rhythm)
3. 💬 **Conversational Reply (Native Style):** (2-3 short, punchy native English sentences)
4. 🎧 **Native Decoding Box:** (Break down native phrases used + Bengali explanation)
5. 📝 **Natural Upgrade:** (How a native speaker would say it more smoothly)
6. 🚀 **Next Challenge:** (Prompt them to reply with voice or text)
"""

    contents = [
        types.Content(
            role="user",
            parts=[
                audio_part,
                types.Part.from_text(text=instruction + mode_instruction)
            ]
        )
    ]

    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
            )
        )
        return response.text or "I listened to your voice message, but couldn't clearly catch the words. Could you speak a bit closer to the microphone?"
    except Exception as e:
        return f"❌ Error processing voice message: {str(e)}"

def generate_image_tutor_reply(
    image_bytes: bytes,
    caption: str = "",
    user_level: str = "Intermediate"
) -> str:
    client = get_client()
    if not client:
        return "⚠️ Gemini API Key পাওয়া যায়নি।"

    image_part = types.Part.from_bytes(data=bytes(image_bytes), mime_type="image/jpeg")

    instruction = f"""
The user sent an image related to learning English, a screenshot of a conversation, an email, or study material.
User's Question / Caption: "{caption if caption else 'Analyze and explain this image for an English learner'}"
User Level: {user_level}

Your task:
1. 🖼️ **Text in the Image (ছবিতে থাকা ইংরেজি লেখা):**
   - Transcribe or summarize the main English text clearly.
2. 🔍 **Detailed Breakdown & Corrections (যদি ভুল থাকে বা কোনো মেসেজ হয়):**
   - If it's a client message/email: explain what the client is asking for, the tone, and subtle meanings.
   - If it's a question/exam problem: give the correct answer with a logical explanation.
   - If it contains mistakes: point them out and give the natural native upgrade.
3. 🎧 **Native Vocabulary & Idioms:**
   - Highlight any important words, idioms, or collocations in the image.
4. 🇧🇩 **বাংলায় সহজ ব্যাখ্যা ও অনুবাদ:**
   - Provide a clear Bengali explanation and translation.
5. 💬 **Suggested Action / Next Step:**
   - If it's a message, give 1-2 ready-to-use professional replies the user can send back!
"""

    contents = [
        types.Content(
            role="user",
            parts=[
                image_part,
                types.Part.from_text(text=instruction)
            ]
        )
    ]

    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="You are Antigravity Multimodal English Vision Specialist.",
                temperature=0.5,
            )
        )
        return response.text or "I processed the image, but couldn't detect clear English text. Please send a clearer screenshot or photo."
    except Exception as e:
        return f"❌ Error reading image: {str(e)}"

def generate_video_tutor_reply(
    video_path: str,
    caption: str = "",
    user_level: str = "Intermediate"
) -> str:
    import time
    client = get_client()
    if not client:
        return "⚠️ Gemini API Key পাওয়া যায়নি।"

    uploaded_file = None
    try:
        uploaded_file = client.files.upload(file=video_path)

        for _ in range(30):
            if uploaded_file.state.name == "ACTIVE":
                break
            if uploaded_file.state.name == "FAILED":
                return "❌ ভিডিওটি প্রসেস করতে ব্যর্থ হয়েছে। দয়া করে আবার চেষ্টা করুন।"
            time.sleep(1)
            uploaded_file = client.files.get(name=uploaded_file.name)

        instruction = f"""
The user sent a short video clip (movie, reel, or spoken English practice).
User's Caption/Goal: "{caption if caption else 'Listen to the speech in this video and break it down'}"
User Level: {user_level}

Your task:
1. 🎬 **Dialogue Transcription (ভিডিওর ইংরেজি সংলাপ):**
   - Transcribe the main English lines spoken in the clip.
2. ⚡ **Native Speech & Sound Secrets (কীভাবে কথাগুলো কানেক্ট করা হয়েছে):**
   - Point out fast speech, blended words, slang, or contractions (e.g. gonna, wanna, kinda, gotta).
3. 🇧🇩 **বাংলায় অর্থ ও কনটেক্সট:**
   - Explain the meaning and humor/emotion in simple Bengali.
4. 🗣️ **Shadowing & Speaking Practice:**
   - Pick 1 punchy sentence from the clip and challenge the user to repeat it aloud!
"""

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=[uploaded_file, instruction],
            config=types.GenerateContentConfig(
                system_instruction="You are Antigravity Video & Spoken English Specialist.",
                temperature=0.6
            )
        )
        return response.text or "Video analysis complete."
    except Exception as e:
        return f"❌ Error analyzing video: {str(e)}"
    finally:
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass

def extract_youtube_id(url: str) -> Optional[str]:
    import re
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:shorts\/)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def analyze_youtube_transcript(url: str, user_level: str = "Intermediate") -> str:
    """Fetches YouTube transcript and generates deep English learning breakdown."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API Key পাওয়া যায়নি।"

    video_id = extract_youtube_id(url)
    if not video_id:
        return "❌ সঠিক YouTube ভিডিও লিংক পাওয়া যায়নি। দয়া করে সঠিক লিংক দিন।"

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.fetch(video_id)
        
        # Combine transcript text
        full_text = " ".join([item.text if hasattr(item, 'text') else item.get('text', '') for item in transcript_list])
        
        # Limit text to ~12000 chars to avoid exceeding telegram/tokens
        truncated_text = full_text[:12000]
    except Exception as e:
        err_msg = str(e)
        if "no longer available" in err_msg or "unavailable" in err_msg.lower():
            return "⚠️ **এই YouTube ভিডিওটি বর্তমানে অনুপলব্ধ বা ডিলিট/প্রাইভেট করা (Video Unavailable)!**\n\nইউটিউবে চেক করে দেখলাম এই ভিডিওটি প্লে করা যাচ্ছে না। অনুগ্রহ করে অন্য কোনো সচল ইংরেজি ভিডিও বা শর্টসের লিংক পাঠিয়ে ট্রাই করুন।"
        elif "disabled" in err_msg.lower() or "no transcript" in err_msg.lower():
            return "⚠️ **এই ভিডিওতে কোনো ইংরেজি সাবটাইটেল বা ট্রান্সক্রিপ্ট পাওয়া যায়নি।**\n\nভিডিওটিতে ক্যাপশন (CC) বন্ধ করা থাকতে পারে। অনুগ্রহ করে ক্যাপশন রয়েছে এমন একটি ভিডিও পাঠান।"
        return f"⚠️ এই YouTube ভিডিওটির ট্রান্সক্রিপ্ট পাওয়া যায়নি।\nকারণ: {err_msg[:200]}"

    prompt = f"""
You are Antigravity YouTube English Coach.
A Bengali learner submitted a YouTube video to learn English from: {url}
Target English Level: {user_level}

TRANSCRIPT EXCERPT:
"{truncated_text}"

Your task:
1. 📜 **Key Dialogue & Highlights (ভিডিওর গুরুত্বপূর্ণ ডায়লগ ও লাইনসমূহ):**
   - Extract the most important 3-5 real-life conversational sentences from the transcript.
2. ⚡ **Native Idioms, Slang & Fast Speech Used:**
   - Point out any connected speech, phrasal verbs, idioms, or native informal expressions used by the speakers.
3. 🇧🇩 **বাংলায় সহজ সারসংক্ষেপ ও অর্থ (Summary & Meaning in Bengali):**
   - Explain what the video was about in simple Bengali so the user understands the whole story.
4. 📝 **Vocabulary Bank:**
   - 3-4 powerful words from the video with Bengali meaning and example sentences.
5. 💬 **Speaking Challenge:**
   - Give the user 1 iconic line from this video to practice speaking out loud!
"""

    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert English teacher analyzing YouTube video transcripts.",
                temperature=0.6,
            )
        )
        return response.text or "YouTube video analysis completed."
    except Exception as e:
        return f"❌ Error analyzing transcript: {str(e)}"

def decode_native_phrase(phrase: str) -> str:
    """Decodes fast native slang/phrases for the user."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
The user heard this phrase from a native speaker (US/UK/Canada/Aus) and couldn't understand it:
"{phrase}"

Provide a crystal-clear native breakdown:
1. 🗣️ **The Phrase:** "{phrase}"
2. 📖 **Literal / Textbook Meaning:** (What books teach)
3. 🇺🇸/🇬🇧 **What Native Speakers ACTUALLY Mean:** (The real meaning in fast/casual English)
4. 🇧🇩 **বাংলায় সহজ ব্যাখ্যা ও ব্যবহার:** (বাস্তব উদাহরণসহ)
5. ⚡ **Connected Speech / Pronunciation Secret:** (How native speakers blend the sounds, e.g. "What do you" -> "Whaddya")
6. 💬 **How to Reply Back:** (Give 2 natural short replies the user can use)
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a Native English Speech Decoder for Bengali learners.",
                temperature=0.6,
            )
        )
        return response.text or "Decoding failed."
    except Exception as e:
        return f"Error: {e}"

def generate_daily_lesson(level: str = "Intermediate") -> str:
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
Generate today's "Native English Secret" for a Bengali learner ({level} level) to understand native speakers from USA/UK/Australia.
Focus on ONE of these:
- Real-world fast spoken shortcut (e.g. "gonna", "wanna", "gotta", "dunno", "lemme", "kinda").
- OR a super common native idiom/phrasal verb (e.g. "I'm beat", "cut it out", "heads up", "no worries", "hit me up").
- OR connected speech sound change (e.g. how "Did you" sounds like "Did-ja").

Format:
1. 🎯 **Today's Native Shortcut / Idiom**
2. 🇺🇸/🇬🇧 **How Native Speakers Say It vs Bookish English**
3. 🇧🇩 **বাংলায় বাস্তব ব্যাখ্যা ও পরিস্থিতি**
4. 💬 **Real Conversation Snippet (২ লাইনের বাস্তব কথোপকথন)**
5. 🚀 **Daily Challenge:** Ask the user to reply using this shortcut!
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are Antigravity Native English Coach.",
                temperature=0.7,
            )
        )
        return response.text or "Lesson generation failed."
    except Exception as e:
        return f"Error creating daily lesson: {e}"

def generate_vocab_card(level: str = "Intermediate") -> str:
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
Provide ONE high-frequency native informal expression, slang, or phrasal verb used daily in USA, UK, Canada, or Australia.
Include:
- 📌 Native Phrase
- 🗣️ Fast Speech Pronunciation (Phonetic guide)
- 📖 Textbook English vs Native English
- 🇧🇩 Bengali Meaning & Cultural Context
- 💬 2 Real-world Short Dialogue Examples
- ✍️ Quick Practice Question for the user to answer.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert native English slang and idioms coach.",
                temperature=0.7,
            )
        )
        return response.text or "Vocabulary generation failed."
    except Exception as e:
        return f"Error: {e}"

def generate_quiz(topic: str = "Native Slang & Connected Speech", level: str = "Intermediate") -> Dict[str, Any]:
    client = get_client()
    if not client:
        return {
            "question": "If an American says: 'I\\'m beat!', what does it mean?",
            "options": ["Someone hit me", "I am very tired", "I lost the game", "I am angry"],
            "correct_index": 1,
            "explanation": "'I\\'m beat' হলো একটি আমেরিকান স্ল্যাং যার অর্থ 'আমি খুবই ক্লান্ত' (Extremely tired)।"
        }

    prompt = f"""
Create an interactive quiz question testing the user's ability to understand NATIVE FAST/CASUAL ENGLISH (slang, idioms, or connected speech like gonna/wanna/beat/down/swamped/gotcha).
Target level: {level}.
Output MUST be valid JSON only, with the following exact keys:
{{
  "question": "The question text, e.g. What does a native speaker mean when they say: '...'?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 0, // integer 0 to 3
  "explanation": "Clear explanation in English and Bengali explaining the native usage and context."
}}
Return ONLY raw JSON, no markdown codeblocks, no extra text.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        text = response.text.strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Quiz generation error: {e}")
        return {
            "question": "If an American says 'I\\'m down for pizza tonight', what does it mean?",
            "options": [
                "I don't like pizza",
                "I am ready and happy to eat pizza",
                "Pizza fell down",
                "I am feeling sad about pizza"
            ],
            "correct_index": 1,
            "explanation": "'I\\'m down' মানে হলো 'আমি রাজি/আমি আগ্রহী' (I'm willing or excited to participate)।"
        }

def translate_banglish_to_native(raw_input: str) -> str:
    """Converts Bengali or Banglish into authentic native English variations."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
The user is a Bengali speaker who wrote their thought in Bengali or Banglish:
"{raw_input}"

Your task:
Transform this Bengali/Banglish thought into 3 authentic, natural NATIVE ENGLISH variations (US/UK style):
1. 🇺🇸 **Casual & Friendly (Slack/WhatsApp/Upwork Chat):**
   - Natural, conversational, everyday American phrasing with common contractions.
2. 📧 **Formal / Business (Client Email & Proposal):**
   - Courteous, professional, structured, and polite.
3. ⚡ **Short & Punchy (Fast 1-liner):**
   - Quick, effortless native one-liner.
4. 🎧 **Native Vocabulary & Idiom Breakdown:**
   - Highlight 1-2 native phrases used.
5. 🇧🇩 **বাংলায় প্রয়োজনীয় টিপস:**
   - কেন এই শব্দগুলো নির্বাচন করা হয়েছে তার সংক্ষিপ্ত ব্যাখ্যা।
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert bilingual Bengali-to-Native English Translator and Communication Coach.",
                temperature=0.5,
            )
        )
        return response.text or "Translation failed."
    except Exception as e:
        return f"Error: {e}"

def generate_pdf_summary(text: str, caption: str = "", user_level: str = "Intermediate") -> str:
    """Summarizes and analyzes English PDF/DOC documents for learning."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    truncated = text[:15000]
    prompt = f"""
You are Antigravity Document English Assistant.
The user uploaded an English document/PDF. User goal/question: "{caption if caption else 'Summarize and explain this document for an English learner'}"
User Level: {user_level}

DOCUMENT CONTENT:
"{truncated}"

Your task:
1. 📄 **Document Summary (মূল বিষয়বস্তু):**
   - 3-4 bullet points summarizing what this document is about.
2. 🔍 **Complex Sentences & Formal Terms Simplified:**
   - Pick 2-3 tricky sentences or formal legal/business terms from the text and explain them in simple English and Bengali.
3. 🇧🇩 **বাংলায় সহজ সারমর্ম (Bengali Summary):**
   - Provide a clear, practical Bengali overview.
4. 💡 **Actionable Recommendation:**
   - If it's a client brief/contract/job description: how the user should reply or prepare for it.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert Document & Business English Analyst.",
                temperature=0.5,
            )
        )
        return response.text or "Document analysis failed."
    except Exception as e:
        return f"Error: {e}"

def generate_shadowing_challenge(user_level: str = "Intermediate") -> Dict[str, Any]:
    """Generates a native speech shadowing prompt."""
    client = get_client()
    if not client:
        return {
            "sentence": "I'm gonna grab a bite to eat, you wanna come along?",
            "phonetic": "Aim gunna grab uh bite tuh eat, yuh wanna come uh-long?",
            "meaning_bn": "আমি একটু কিছু খেতে যাচ্ছি, তুমিও কি সাথে আসবে?",
            "focus": "Gonna (Going to) এবং Wanna (Want to) এর কানেক্টেড স্পিচ ফ্লো।"
        }

    prompt = f"""
Generate 1 punchy, real-world native English sentence for a speech shadowing exercise ({user_level} level).
Must be valid JSON only with exact keys:
{{
  "sentence": "The native sentence with contractions (e.g. gonna, wanna, coulda, kinda)",
  "phonetic": "How it actually sounds phonetically in fast connected speech",
  "meaning_bn": "Clear meaning in Bengali",
  "focus": "The specific connected speech sound to practice (e.g. reduction, blending)"
}}
Return raw JSON only.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        return {
            "sentence": "To be honest, I couldn't care less about what they say.",
            "phonetic": "Tuh be honest, I couldn-care less...",
            "meaning_bn": "সত্যি বলতে, তারা কী বলে তা নিয়ে আমার বিন্দুমাত্র মাথাব্যথা নেই।",
            "focus": "'Couldn't care less' নেটিভ ইডিয়মের ব্যবহার।"
        }

def generate_interview_turn(scenario: str, history: List[Dict[str, str]], user_reply: str) -> str:
    """Conducts a realistic live interview simulation turn."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
You are conducting a realistic English Interview simulation with a Bengali candidate.
Scenario: {scenario}

Candidate's latest answer: "{user_reply}"

Your task:
1. 🔍 **Brief Feedback on Candidate's Answer (১-২ লাইনে ফিডব্যাক):**
   - Point out if their answer was clear, professional, or if they used any awkward phrasing. Suggest a top 1% native way to say it.
2. 🎭 **In-Character Follow-up Question (পরবর্তী প্রশ্ন):**
   - Stay strictly in character as the foreign client or hiring manager and ask the next natural question.
   - Keep questions realistic, conversational, and challenging!
3. 💡 **Pro-Tip in Bengali:**
   - এক লাইনে বাংলায় পরামর্শ দিন যে এই ধরনের প্রশ্নের উত্তর কীভাবে দেওয়া উচিত।
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert Foreign Client & Hiring Manager.",
                temperature=0.7,
            )
        )
        return response.text or "Could you elaborate on that?"
    except Exception as e:
        return f"Error: {e}"

def generate_interview_report(conversation_text: str) -> str:
    """Generates final interview scorecard and evaluation."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
Analyze this completed mock interview and provide a comprehensive candidate performance report:
"{conversation_text}"

Provide:
1. 🏆 **Overall Interview Score**: (out of 10)
   - Fluency & Confidence: /10
   - Professional Vocabulary: /10
   - Grammar & Sentence Structure: /10
2. 🌟 **Strongest Points**: What the candidate did well.
3. ⚠️ **Areas for Improvement**: 2-3 repeated mistakes or hesitation patterns.
4. 💎 **Golden Advice in Bengali**: ৩টি গুরুত্বপূর্ণ পরামর্শ যা পরবর্তী রিয়েল ক্লায়েন্ট ইন্টারভিউতে বায়ারকে মুগ্ধ করতে সাহায্য করবে।
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an Elite Executive Interview Coach.",
                temperature=0.5
            )
        )
        return response.text or "Scorecard generation complete."
    except Exception as e:
        return f"Error: {e}"

def analyze_sentence_deep(sentence: str) -> str:
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
The user wants to transform this textbook/bookish sentence into REAL NATIVE CASUAL ENGLISH (how people talk in USA/UK/Canada/Australia):
"{sentence}"

Provide:
1. 🎯 **Natural Native Upgrades**:
   - 🇺🇸 Casual/Everyday (How friends talk):
   - ⚡ Fast Shortened Version (Connected/Slang style):
   - 💼 Professional/Workplace Native:
2. 🔍 **Why the original sounds bookish or unnatural**:
3. 🇧🇩 **বাংলায় সহজ ব্যাখ্যা**:
4. 💬 **Bonus Native Pro-Tip**:
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a Native English Transformation Specialist.",
                temperature=0.5
            )
        )
        return response.text or "Sentence analysis failed."
    except Exception as e:
        return f"Error analyzing sentence: {e}"

def polish_client_message(raw_text: str) -> str:
    """Transforms rough thought/notes into polished, polite, natural client communications."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
The user is a professional freelancer/developer/analyst who needs to communicate with foreign clients (US/UK/Canada/Europe).
They have this rough thought or draft:
"{raw_text}"

Convert it into natural, highly professional, polite native client communications:
1. 💬 **Quick Slack / Upwork Message (ক্যাজুয়াল অথচ প্রফেশনাল চ্যাট):**
   - Natural, concise, friendly American style.
2. 📧 **Formal Email Version (অফিসিয়াল ইমেইল রূপ):**
   - Clear subject line, professional greeting, structured body, polite call-to-action.
3. 🔍 **Key Phrases Used (প্রয়োজনীয় ফ্রেজসমূহ):**
   - Point out 2-3 native workplace phrases used (e.g. "loop in", "touch base", "heads up", "circle back").
4. 🇧🇩 **বাংলায় প্রয়োজনীয় টিপস:**
   - কেন এই টোনটি বায়ারকে সন্তুষ্ট করবে তার সংক্ষিপ্ত ব্যাখ্যা।
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a Native Workplace & Client Communication Specialist.",
                temperature=0.5
            )
        )
        return response.text or "Client message formatting failed."
    except Exception as e:
        return f"Error: {e}"

def generate_listening_challenge() -> Dict[str, Any]:
    """Generates a connected speech listening challenge with text to be spoken by TTS."""
    client = get_client()
    if not client:
        return {
            "spoken_audio_text": "Whatcha reckon we do about it?",
            "question": "Did you catch what was said in the audio?",
            "options": [
                "What do you think we should do about it?",
                "Watch out before we do it",
                "What did you record about it?",
                "Where are you going right now?"
            ],
            "correct_index": 0,
            "explanation": "'Whatcha reckon' হলো ব্রিটিশ/অস্ট্রেলিয়ান ফাস্ট স্পিচ, যার অর্থ 'What do you think/reckon?' (তুমি কী মনে করো?)"
        }

    prompt = """
Generate a fast, connected-speech audio challenge representing how native speakers (US/UK/Aus) blend sounds together in daily life.
Examples of connected speech:
- "Did you eat yet?" -> "Jeet yet?"
- "What do you want to do?" -> "Whaddya wanna do?"
- "Give it to me" -> "Gimme it"
- "Could you give me a hand?" -> "Couldja gimme a hand?"

Return valid JSON with:
{
  "spoken_audio_text": "The exact short sentence to be pronounced by TTS",
  "question": "What does this native fast-speech phrase mean in standard English?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 0,
  "explanation": "Clear explanation of how the sounds connected/blended and the Bengali meaning."
}
Return raw JSON only.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        return {
            "spoken_audio_text": "Whaddya wanna do tonight?",
            "question": "What does 'Whaddya wanna do tonight?' mean?",
            "options": [
                "What do you want to do tonight?",
                "What did you want to do yesterday?",
                "Where are you going tonight?",
                "Who do you want to meet tonight?"
            ],
            "correct_index": 0,
            "explanation": "'Whaddya wanna' হলো 'What do you want to' এর ফাস্ট আমেরিকান কানেক্টেড স্পিচ রূপ।"
        }

def generate_upwork_proposal(job_text: str) -> str:
    """Generates a high-converting, buyer-psychology matched Upwork proposal for Web Analytics/Tracking jobs."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
You are an Elite Upwork Proposal Strategist who has won hundreds of high-ticket ($50-$120/hr) contracts for Web Analytics, Google Tag Manager (GTM), GA4, Meta Conversion API (CAPI), and Server-side Tracking.

Analyze this client job post carefully:
\"\"\"{job_text}\"\"\"

Generate a winning, human, casual-yet-expert proposal tailored to the client's country and psychological state:

1. 🎯 **Buyer Psychology & Country Profile (বায়ার প্রোফাইল):**
   - Detect likely country (US / UK / Australia / Germany / Europe) from language, spelling, or context.
   - What does this buyer truly care about? (e.g. Fast turnaround, clean ROAS tracking, privacy/GDPR compliance, or stopping double counting).

2. 🎣 **The Killer 2-Line Hook (প্রথম ২ লাইন যা বায়ার নোটিফিকেশনে দেখবে):**
   - Must NOT start with "Hi, I am an expert" or generic flattery.
   - Jump straight into the technical symptom and relief (e.g. "Hey [Name], saw your CAPI deduplication is misfiring in Meta Events Manager — that's usually because the browser and server event_id tokens aren't identical.").

3. 💼 **The Complete Winning Proposal (সম্পূর্ণ প্রপোজাল):**
   - Natural native conversational tone (US or UK style based on client).
   - Crisp 3-bullet action plan.
   - Relevant proof/quick case study.
   - Ultra-low friction closing question (e.g. "Do you have Stape or GCP container set up already? Drop me a quick ping and we can knock this out today.").

4. 🇧🇩 **সাইকোলজিক্যাল টিপস (কেন এই প্রপোজালটি কাজ করবে):**
   - ৩টি গুরুত্বপূর্ণ পয়েন্ট বাংলায় ব্যাখ্যা করুন যা ইন্টারভিউ কল পাওয়ার সম্ভাবনা বাড়িয়ে দেয়।
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a World-Class Freelancing Proposal Copywriter.",
                temperature=0.6
            )
        )
        return response.text or "Proposal generation failed."
    except Exception as e:
        return f"Error generating proposal: {e}"

def generate_call_lifeline(buyer_question: str) -> Dict[str, str]:
    """Generates an instant 2-3 sentence emergency speech script for live Zoom/Meet client calls."""
    client = get_client()
    if not client:
        return {
            "spoken_script": "That's a great question. Typically when that happens, the tracking tag is firing before the dataLayer push completes. I can audit the GTM container in preview mode right now.",
            "follow_up": "Would you mind sharing screen or sending me temporary viewer access?",
            "bangla_tip": "আত্মবিশ্বাসের সাথে বলুন এবং সাথে সাথে স্ক্রিন শেয়ার চান যাতে বল আপনার কোর্টে আসে।",
            "tts_text": "That's a great question. Typically when that happens, the tracking tag is firing before the dataLayer push completes."
        }

    prompt = f"""
The user is live on a Zoom/Google Meet call with a foreign client.
The client just asked this technical or business question:
\"\"\"{buyer_question}\"\"\"

Provide an immediate emergency spoken script:
Return valid JSON with:
{{
  "spoken_script": "2-3 short, ultra-fluent, confident native sentences to say out loud right now without hesitation.",
  "follow_up": "1 smart follow-up question to ask the client to keep control of the conversation.",
  "bangla_tip": "বাংলায় ছোট্ট টিপস: কেন এই উত্তরটি বায়ারের আস্থা অর্জন করবে।",
  "tts_text": "The exact spoken_script for audio pronunciation practice."
}}
Return raw JSON only.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        return {
            "spoken_script": f"Understood. Let me check the event payload directly in the tag debugger. {buyer_question}",
            "follow_up": "Could you grant me temporary access to your GTM workspace?",
            "bangla_tip": "ভয় না পেয়ে সরাসরি ডিবাগার চেক করার কথা বলুন।",
            "tts_text": "Understood. Let me check the event payload directly in the tag debugger."
        }

def analyze_screen_explain(image_bytes: bytes, mime_type: str, caption: str = "") -> str:
    """Inspects technical dashboards (GTM/GA4/Meta Ads) and crafts how to explain it to a client."""
    client = get_client()
    if not client:
        return "⚠️ Gemini API key missing."

    prompt = f"""
Analyze this technical screenshot (likely Google Tag Manager, GA4, Meta Events Manager, BigQuery, or tracking dashboard).
User's note/caption: "{caption}"

Provide:
1. 🔍 **Technical Diagnosis (স্ক্রিনশটে কী দেখা যাচ্ছে):**
   - Identify metrics, errors, or configuration status accurately.

2. 🗣️ **How to Explain This to Your Client in Spoken English (বায়ারকে মুখে কী বলবেন):**
   - Provide a 3-4 sentence natural, non-jargon spoken script you can tell the client on Zoom or write in Slack.
   - Example: "Hey, looking at your Events Manager, the browser pixel is firing purchase events properly, but the server container is receiving a null transaction_id. That's why your event match quality is low."

3. 🛠️ **Recommended Fix & Action Items (সমাধানের ধাপ):**
   - 2-3 bullet points on how to fix it in GTM or the server container.

4. 🇧🇩 **বাংলায় সারমর্ম ও পরামর্শ:**
   - বায়ারের সামনে তোতলাতে না হওয়ার জন্য সহজ বাংলায় মূল বিষয়।
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                types.Part.from_text(text=prompt)
            ],
            config=types.GenerateContentConfig(
                system_instruction="You are an Expert Web Analytics & Client Communication Mentor.",
                temperature=0.4
            )
        )
        return response.text or "Could not analyze screenshot."
    except Exception as e:
        return f"Error analyzing technical screenshot: {e}"

def analyze_phonetics_deep(audio_bytes: bytes, mime_type: str) -> Dict[str, Any]:
    """Listens to speech and performs detailed phonetics & accent audit for Bengali speakers."""
    client = get_client()
    if not client:
        return {
            "transcript": "Audio received",
            "clarity_score": 8,
            "markdown": "⚠️ Gemini API key missing for phonetics analysis.",
            "drill_text": "Very well, water the vines."
        }

    prompt = """
Listen to this spoken audio carefully. The speaker is an English learner from Bangladesh.
Analyze their phonetics, pronunciation, and intonation:

Check specifically for common South Asian / Bengali speech habits:
1. /v/ vs /w/ confusion (pronouncing "very" as "wery" or "water" as "vater").
2. /th/ sound (/θ/ in think, /ð/ in that) vs dental /t/ or /d/.
3. /r/ pronunciation (American rhotic curl vs British non-rhotic vs rolled Bengali 'র').
4. Dropping word endings (omitting final -t, -d, -s, -ed).
5. Vowel length and sentence rhythm (stress-timed vs syllable-timed).

Return valid JSON with:
{
  "transcript": "Exact transcription of what the user said",
  "clarity_score": 8, // Integer 1-10
  "phonetic_breakdown": [
    {
      "word": "water",
      "target_sound": "/w/",
      "user_sound": "/v/",
      "status": "yellow", // green, yellow, or red
      "tip_bn": "ঠোঁট গোল করে বাঁশির মতো ফুঁ দিয়ে 'ওয়াটার' বলুন, দাঁত দিয়ে ঠোঁট কামড়াবেন না।"
    }
  ],
  "drill_text": "A short 5-word sentence to practice the weak sound",
  "overall_feedback_bn": "২-৩ লাইনে সামগ্রিক উচ্চারণ ও অ্যাকসেন্টের ফিডব্যাক বাংলায়।"
}
Return raw JSON only.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                types.Part.from_text(text=prompt)
            ],
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        return {
            "transcript": "Speech detected",
            "clarity_score": 7,
            "phonetic_breakdown": [],
            "drill_text": "Practice saying: Think through the thick thoughts.",
            "overall_feedback_bn": f"উচ্চারণ নিরীক্ষা সম্পন্ন: {e}"
        }

def simulate_scenario_turn(scenario_type: str, history: List[Dict[str, str]], user_reply: str) -> Dict[str, Any]:
    """Simulates real-world difficult client negotiation scenarios."""
    client = get_client()
    if not client:
        return {
            "client_reply": "Let me think about that.",
            "feedback": "Keep your arguments value-focused.",
            "tip_bn": "নিজের কাজের ভ্যালু তুলে ধরুন।"
        }

    scenario_descriptions = {
        "rate": "Budget & Hourly Rate Negotiation: The user is currently at $30/hr and is negotiating to increase to $60/hr due to deep GTM server-side and attribution expertise. The client is a budget-conscious US business owner.",
        "angry": "Calming an Angry Client: The client is furious because their Facebook ad conversions dropped 40% after iOS update, thinking tracking is completely broken. The user needs to calm them down with confidence, explain why it happened, and present the server-side solution.",
        "smalltalk": "Zoom Pre-Meeting Small Talk: Casual 2-minute icebreaker before talking shop. Client talks about NFL, crazy weather in Chicago, or weekend plans. User needs to sound natural, relaxed, and culturally fluent.",
        "scope": "Scope Creep Defense: The client wants 5 new domain setups and CRM integrations done for free within the original basic audit budget. User needs to politely but firmly push back and upsell an add-on milestone."
    }

    desc = scenario_descriptions.get(scenario_type, scenario_descriptions["rate"])

    prompt = f"""
You are the client in this realistic simulation:
Scenario: {desc}

Conversation so far:
{json.dumps(history[-6:], indent=2)}

User just said:
"{user_reply}"

Return valid JSON with:
{{
  "client_reply": "In-character realistic response as the client (natural American colloquial English, push back or agree based on user's diplomacy).",
  "user_performance_score": 8, // 1-10
  "diplomacy_feedback": "Short feedback on user's tone, firmness, and natural English phrasing.",
  "recommended_next_saying": "A native way to counter or respond to what you just said.",
  "tip_bn": "বাংলায় স্ট্র্যাটেজিক টিপস যা রিয়েল ক্লায়েন্টের সাথে কার্যকর হবে।"
}}
Return raw JSON only.
"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        return {
            "client_reply": "Hmm, I see where you're coming from, but that seems a bit steep. What makes this different from what an agency would do?",
            "user_performance_score": 7,
            "diplomacy_feedback": "Good attempt, but make sure to anchor on ROI.",
            "recommended_next_saying": "I totally get that. The reason is that server-side tracking recovers lost ad attribution by up to 25%, which directly drops your CPA.",
            "tip_bn": "সবসময় ক্লায়েন্টের লাভ এবং আরও বেশি সেলস আনার পয়েন্টে ফোকাস করুন।"
        }
