import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import config
import database
import mentor_ai
import scheduler
import tts_service

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Temporary memory for active quizzes (key: chat_id, val: quiz_data)
active_quizzes = {}

VOICE_MAP = {
    "US": "en-US-ChristopherNeural",
    "UK": "en-GB-RyanNeural",
    "AUS": "en-AU-WilliamNeural"
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    db_user = database.get_or_create_user(
        user_id=user.id,
        chat_id=chat_id,
        username=user.username or "",
        first_name=user.first_name or "Friend"
    )

    welcome_text = (
        f"👋 **Hello {user.first_name}! Welcome to Antigravity English Mentor!** 🇬🇧🇧🇩\n\n"
        "আমি আপনার ২৪/৭ পার্সোনাল ইংলিশ টিউটর ও মেন্টর। আপনি টেলিগ্রাম দিয়ে যেকোনো সময় আমার সাথে ইংলিশ প্র্যাকটিস করতে পারবেন এবং আপনার সব পড়া নিয়ন্ত্রণ করতে পারবেন।\n\n"
        "💡 **আমি আপনাকে যেভাবে সাহায্য করব:**\n"
        "1. 💬 **২৪/৭ চ্যাট:** আপনি আমার সাথে যেকোনো বিষয়ে ইংরেজিতে কথা বলতে পারেন। কোনো ভুল হলে আমি সাথে সাথে সুন্দরভাবে ভুল ধরিয়ে দিব ও বাংলায় বুঝিয়ে দিব।\n"
        "2. 🌅 **প্রতিদিনের লেসন:** প্রতিদিন সকাল ৯টায় নতুন লেসন এবং রাত ৮টায় ভোকাবুলারি পাবেন।\n"
        "3. 🧠 **কুইজ ও এক্সারসাইজ:** `/quiz` দিলে সাথে সাথে ইন্টারঅ্যাক্টিভ কুইজ আসবে।\n"
        "4. 🔍 **সেন্টেন্স চেক:** `/correct আপনার বাক্য` লিখলে সেন্টেন্সের ভুলত্রুটি বিশ্লেষণ করে দিব।\n\n"
        "🎯 **শুরু করার জন্য আপনার বর্তমান লেভেল নির্বাচন করুন:**"
    )

    keyboard = [
        [
            InlineKeyboardButton("🌱 Beginner (প্রাথমিক)", callback_data="set_level_Beginner"),
            InlineKeyboardButton("🌿 Intermediate (মধ্যম)", callback_data="set_level_Intermediate"),
        ],
        [
            InlineKeyboardButton("🌳 Advanced (উন্নত)", callback_data="set_level_Advanced"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 **Antigravity English Mentor - পাওয়ারফুল ফিচারসমূহ:**\n\n"
        "💼 **ফ্রিল্যান্সিং, আপওয়ার্ক ও ক্লায়েন্ট কল (New!):**\n"
        "• `/proposal <জব পোস্ট>` - বায়ারের দেশ ও সাইকোলজি বুঝে উইনিং প্রপোজাল তৈরি\n"
        "• `/callhelp <বায়ারের প্রশ্ন>` - লাইভ জুমে মুখে বলার মতো ২ লাইনের জরুরি স্পিচ ও অডিও\n"
        "• `/screenexplain` - GA4/GTM/CAPI এরর স্ক্রিনশট বায়ারকে মুখে বুঝিয়ে বলার স্ক্রিপ্ট\n"
        "• `/scenario` - কঠিন পরিস্থিতি নেগোসিয়েশন সিমুলেটর (রেট বৃদ্ধি, রাগী বায়ার শান্ত করা, স্মলটক)\n"
        "• `/endscenario` - রানিং সিনারিও সিমুলেশন বন্ধ করা\n"
        "• `/client <মেসেজ>` - রাফ টেক্সটকে বায়ারের মন জয় করার মতো নেটিভ মেসেজে রূপান্তর\n"
        "• `/interview` - লাইভ বায়ার কল ও জব ইন্টারভিউ সিমুলেটর (শেষে `/endinterview`)\n\n"
        "🎧 **নেটিভ স্পিচ, অ্যাকসেন্ট ও ফোনেটিক্স:**\n"
        "• `/phonetics` - অ্যাকসেন্ট অডিট গাইড ও ৫টি প্রধান উচ্চারণ ত্রুটি সমাধান\n"
        "• `/listen` - কানেক্টেড স্পিচ ও ফাস্ট নেটিভ স্পোকেন অডিও টেস্ট\n"
        "• `/shadow` - স্পিচ শ্যাডোয়িং ট্রেনিং (অডিও শুনে হুবহু মুখে রিপিট করা)\n"
        "• `/decode <বাক্য>` - যেকোনো নেটিভ স্ল্যাং/শর্টকাট ডিকোড করা\n"
        "• `/speak <বাক্য>` - যেকোনো বাক্যের আসল নেটিভ উচ্চারণ অডিও আকারে শোনা\n"
        "• `/accent` - অ্যাকসেন্ট নির্বাচন (American / British / Australian)\n"
        "• `/voice on|off` - স্বয়ংক্রিয় ভয়েস রিপ্লাই চালু বা বন্ধ রাখা\n\n"
        "🧠 **স্মৃতি ও স্পেসড-রিপিটিশন:**\n"
        "• `/skills` - ৬টি সম্পূর্ণ ইংলিশ লার্নিং স্কিলস ক্যাটালগ (অ্যাকসেন্ট, ক্লায়েন্ট প্লেবুক, স্ল্যাং, আইইএলটিএস, গ্রামার, টেকনিক্যাল)\n"
        "• `/srs` - Ebbinghaus স্পেসড-রিপিটিশন ফ্ল্যাশ কার্ড কুইজ (ভুলে যাওয়ার আগেই প্র্যাকটিস)\n"
        "• `/review` - আপনার অতীত ভুলের ফ্ল্যাশ কার্ড\n"
        "• `/quiz` - নেটিভ স্পিচ কুইজ\n"
        "• `/vocab` - আজকের নতুন স্ল্যাং বা ফ্রেজ\n"
        "• `/stats` - স্ট্রিক ও অগ্রগতি\n\n"
        "🌐 **টেলিগ্রাম মিনি অ্যাপ ও ওয়েব হাব:**\n"
        "• `/app` - লাইভ ওয়েব স্টুডিও ও অডিও কলার (tutor.sakibhossain.io)\n"
        "• চ্যাট বারের পাশে **'🚀 Web Studio'** বাটনে চাপ দিয়ে যেকোনো সময় মিনি অ্যাপ ওপেন করতে পারেন!\n\n"
        "🎙️ **টিপ:** আপনি যেকোনো সময় মুখে কথা বলে **ভয়েস মেসেজ** পাঠাতে পারেন! বট আপনার অ্যাকসেন্ট ও গ্রামার স্ক্যান করে নেটিভ ভয়েসে অডিও রিপ্লাই দেবে।"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def decode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🎧 আপনি নেটিভ স্পিকারদের যে শর্টকাট বা ফ্রেজ বুঝতে পারেননি তা লিখুন।\n\nউদাহরণ:\n• `/decode I'm beat`\n• `/decode Whatcha up to?`\n• `/decode I'm swamped`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    phrase = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    decoded = await asyncio.to_thread(mentor_ai.decode_native_phrase, phrase)
    await update.message.reply_text(decoded, parse_mode=ParseMode.MARKDOWN)

async def client_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "💼 ক্লায়েন্টকে কী বলতে চান তা বাংলায় বা ভাঙা ইংরেজিতে লিখুন।\n\nউদাহরণ:\n`/client I am not able to track purchase event in GA4 because datalayer not firing. please check developer.`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    raw_text = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    result = await asyncio.to_thread(mentor_ai.polish_client_message, raw_text)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

async def youtube_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🎬 যেকোনো ইংরেজি YouTube ভিডিও বা Shorts-এর লিংক দিন।\n\nউদাহরণ:\n`/yt https://youtu.be/...`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url = context.args[0].strip()
    user_id = update.effective_user.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=update.effective_chat.id)
    level = db_user.get("level", "Intermediate")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_text("⏳ ভিডিওটির ট্রান্সক্রিপ্ট সংগ্রহ ও বিশ্লেষণ করা হচ্ছে, দয়া করে কয়েক সেকেন্ড অপেক্ষা করুন...")

    result = await asyncio.to_thread(mentor_ai.analyze_youtube_transcript, url, level)
    try:
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning(f"Markdown send failed on youtube reply: {e}")
        await update.message.reply_text(result)

async def bn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🇧🇩 আপনার মনের কথাটি বাংলায় বা বাংলিশে লিখুন।\n\nউদাহরণ:\n• `/bn ami client ke bolte chai tracking setup done, ekhon test korte hobe`\n• `/bn kalke amra shobai eksathe dekha korbo`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    raw_input = " ".join(context.args)
    user_id = update.effective_user.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=update.effective_chat.id)
    accent = db_user.get("accent", "US")
    voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    result = await asyncio.to_thread(mentor_ai.translate_banglish_to_native, raw_input)

    try:
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning(f"Markdown send failed on bn reply: {e}")
        await update.message.reply_text(result)

    # Send voice note of the casual version
    audio_bytes = await tts_service.text_to_speech_bytes(result, voice=voice)
    if audio_bytes:
        try:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=audio_bytes, caption="🎙️ নেটিভ উচ্চারণ শুনুন:")
        except Exception as e:
            logger.error(f"Voice send failed: {e}")

async def shadow_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=chat_id)
    level = db_user.get("level", "Intermediate")
    accent = db_user.get("accent", "US")
    voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.RECORD_VOICE)
    challenge = await asyncio.to_thread(mentor_ai.generate_shadowing_challenge, level)

    sentence = challenge.get("sentence", "I gotta get going now.")
    phonetic = challenge.get("phonetic", "")
    meaning_bn = challenge.get("meaning_bn", "")
    focus = challenge.get("focus", "")

    audio_bytes = await tts_service.text_to_speech_bytes(sentence, voice=voice)

    msg = (
        f"🎙️ **Speech Shadowing Practice (স্পিকিং স্পিড ও অ্যাকসেন্ট ট্রেনিং)**\n\n"
        f"🎯 **Target Sentence:**\n`{sentence}`\n\n"
        f"🗣️ **Phonetic (উচ্চারণ গাইড):** *{phonetic}*\n"
        f"🇧🇩 **বাংলা অর্থ:** {meaning_bn}\n"
        f"⚡ **ফোকাস পয়েন্ট:** {focus}\n\n"
        f"👇 **আপনার কাজ:** নিচের অডিওটি মনোযোগ দিয়ে ৩-৪ বার শুনুন। তারপর অডিওর মতো হুবহু স্পিড ও টানে **একটি ভয়েস মেসেজ পাঠিয়ে রিপ্লাই দিন!**"
    )

    if audio_bytes:
        await context.bot.send_voice(chat_id=chat_id, voice=audio_bytes)
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def interview_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💼 Freelance Client Call (Upwork/Fiverr)", callback_data="start_interview_client"),
        ],
        [
            InlineKeyboardButton("🏢 Tech / Web Analyst Job Interview", callback_data="start_interview_tech"),
        ],
        [
            InlineKeyboardButton("✈️ US/UK Visa & Immigration Interview", callback_data="start_interview_visa"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = (
        "🎭 **রিয়েল-লাইভ ইংলিশ ইন্টারভিউ সিমুলেটর!**\n\n"
        "আমি সরাসরি আপনার বিদেশি বায়ার বা ইন্টারভিউয়ারের ভূমিকা পালন করব। আমি একটি করে প্রশ্ন করব এবং আপনি টেক্সট বা **ভয়েস মেসেজে** উত্তর দেবেন।\n\n"
        "ইন্টারভিউ শেষ করতে যেকোনো সময় লিখবেন: `/endinterview` (শেষে আপনার স্কোরকার্ড ও বিশ্লেষণ পাবেন)।\n\n"
        "👇 কোন বিষয়ে ইন্টারভিউ প্র্যাকটিস করতে চান বেছে নিন:"
    )
    await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def endinterview_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    current_state = database.get_interview_state(user_id)

    if not current_state:
        await update.message.reply_text("⚠️ আপনার কোনো সক্রিয় ইন্টারভিউ চলছে না। নতুন ইন্টারভিউ শুরু করতে লিখুন: `/interview`")
        return

    # Clear state
    database.set_interview_state(user_id, "")
    history = database.get_chat_history(user_id, limit=12)
    conv_text = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in history])

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    report = await asyncio.to_thread(mentor_ai.generate_interview_report, conv_text)

    await update.message.reply_text(f"🏁 **ইন্টারভিউ সমাপ্ত! নিচে আপনার বিস্তারিত স্কোরকার্ড:**\n\n{report}", parse_mode=ParseMode.MARKDOWN)

async def review_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    recent_mistakes = database.get_recent_mistakes(user_id, limit=3)

    if not recent_mistakes:
        await update.message.reply_text(
            "🎉 **চমৎকার! আপনার সাম্প্রতিক কোনো রেকর্ড করা ভুল পাওয়া যায়নি।**\n\nচ্যাটে সাধারণ ইংরেজি প্র্যাকটিস চালিয়ে যান, কোনো ভুল হলে মেন্টর তা স্বয়ংক্রিয়ভাবে সেভ করে রাখবে।",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    msg = "📚 **আপনার পার্সোনাল মিস্টেক রিভিউ (Spaced Repetition):**\n\nগত কয়েকদিনে আপনার করা কিছু গুরুত্বপূর্ণ ভুল নিচে দেওয়া হলো। এগুলো মনে রাখুন যাতে আর ভুল না হয়:\n\n"
    for i, m in enumerate(recent_mistakes, 1):
        msg += (
            f"**{i}. ভুলটি ছিল:**\n"
            f"❌ *{m['original_text']}*\n"
            f"✅ **সঠিক রূপ:** `{m['corrected_text']}`\n"
            f"💡 *কারণ:* {m['explanation']}\n\n"
        )
    msg += "💪 চেষ্টা করুন এই বাক্যগুলো নতুন করে সঠিক নিয়মে একটি মেসেজে লিখে আমাকে রিপ্লাই দিতে!"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.document:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id
    doc = update.message.document
    caption = update.message.caption or ""
    file_name = doc.file_name or "document.txt"

    # Check file size (< 15MB)
    if doc.file_size and doc.file_size > 15 * 1024 * 1024:
        await update.message.reply_text("⚠️ ডকুমেন্টের সাইজ সর্বোচ্চ ১৫ মেগাবাইট (15MB) পর্যন্ত হতে পারে।")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    temp_path = f"/tmp/doc_{user.id}_{doc.file_id[:8]}_{file_name}"
    try:
        doc_file = await context.bot.get_file(doc.file_id)
        await doc_file.download_to_drive(temp_path)
    except Exception as e:
        logger.error(f"Error downloading doc: {e}")
        await update.message.reply_text("❌ ডকুমেন্ট ডাউনলোড করতে সমস্যা হয়েছে।")
        return

    # Extract text from PDF or TXT
    extracted_text = ""
    try:
        if file_name.lower().endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(temp_path)
            extracted_text = "\n".join([page.extract_text() or "" for page in reader.pages[:10]]) # read up to 10 pages
        else:
            with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
                extracted_text = f.read(15000)
    except Exception as e:
        logger.error(f"Error parsing document: {e}")
        extracted_text = ""

    # Clean up local file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not extracted_text.strip():
        await update.message.reply_text("❌ ডকুমেন্টটি থেকে ইংরেজি টেক্সট পড়তে পারা যায়নি (হয়তো এটি স্ক্যান করা ইমেজ বা পাসওয়ার্ড প্রটেক্টেড)।")
        return

    db_user = database.get_or_create_user(user_id=user.id, chat_id=chat_id)
    level = db_user.get("level", "Intermediate")

    reply = await asyncio.to_thread(
        mentor_ai.generate_pdf_summary,
        text=extracted_text,
        caption=caption,
        user_level=level
    )

    try:
        await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning(f"Markdown send failed on doc reply: {e}")
        await update.message.reply_text(reply)

async def speak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🗣️ আপনি যে শব্দ বা বাক্যের আসল নেটিভ উচ্চারণ শুনতে চান তা লিখুন।\nউদাহরণ: `/speak comfortably` অথবা `/speak I'm gonna hit the sack`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    text = " ".join(context.args)
    user_id = update.effective_user.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=update.effective_chat.id)
    accent = db_user.get("accent", "US")
    voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.RECORD_VOICE)
    audio_bytes = await tts_service.text_to_speech_bytes(text, voice=voice)
    
    if audio_bytes:
        await update.message.reply_voice(
            voice=audio_bytes,
            caption=f"🎙️ **Native Pronunciation ({accent} Accent)**\n`{text}`",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("❌ অডিও তৈরি করতে সমস্যা হয়েছে।")

async def listen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=chat_id)
    accent = db_user.get("accent", "US")
    voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.RECORD_VOICE)
    challenge = await asyncio.to_thread(mentor_ai.generate_listening_challenge)
    active_quizzes[chat_id] = challenge

    spoken_text = challenge.get("spoken_audio_text", "Whaddya wanna do?")
    audio_bytes = await tts_service.text_to_speech_bytes(spoken_text, voice=voice)

    question_text = f"🎧 **Ear-Training Challenge:**\n\n{challenge.get('question', '')}\n\nঅডিওটি শুনুন এবং সঠিক অর্থ নির্বাচন করুন:"
    options = challenge.get("options", [])

    keyboard = []
    for i, opt in enumerate(options):
        keyboard.append([InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"quiz_ans_{i}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if audio_bytes:
        await context.bot.send_voice(
            chat_id=chat_id,
            voice=audio_bytes,
            caption="⚡ ফাস্ট নেটিভ স্পিচ অডিও (কানে হেডফোন দিয়ে শুনুন):"
        )
    await update.message.reply_text(question_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def accent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 American Accent (US)", callback_data="set_accent_US"),
        ],
        [
            InlineKeyboardButton("🇬🇧 British Accent (UK)", callback_data="set_accent_UK"),
        ],
        [
            InlineKeyboardButton("🇦🇺 Australian Accent (Aus)", callback_data="set_accent_AUS"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎙️ **আপনার পছন্দের নেটিভ অ্যাকসেন্ট বেছে নিন:**", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def voice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text(
            "🔊 ভয়েস রেসপন্স চালু বা বন্ধ করতে লিখুন:\n• `/voice on` (বট টেক্সটের সাথে সাথে আসল ভয়েস পাঠাবে)\n• `/voice off` (শুধু টেক্সট পাঠাবে)"
        )
        return

    arg = context.args[0].lower().strip()
    if arg == "on":
        database.update_user_voice(user_id, 1)
        await update.message.reply_text("✅ **ভয়েস রেসপন্স সক্রিয় করা হয়েছে!** এখন থেকে বট প্রতিটি উত্তরের সাথে নেটিভ অডিও ভয়েস নোট পাঠাবে।")
    elif arg == "off":
        database.update_user_voice(user_id, 0)
        await update.message.reply_text("🔇 **ভয়েস রেসপন্স বন্ধ করা হয়েছে।** বট এখন শুধু টেক্সট পাঠাবে।")
    else:
        await update.message.reply_text("দয়া করে লিখুন `/voice on` অথবা `/voice off`")

async def lesson_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=update.effective_chat.id)
    level = db_user.get("level", "Intermediate")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    lesson = await asyncio.to_thread(mentor_ai.generate_daily_lesson, level)
    await update.message.reply_text(lesson, parse_mode=ParseMode.MARKDOWN)

async def vocab_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=update.effective_chat.id)
    level = db_user.get("level", "Intermediate")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    vocab = await asyncio.to_thread(mentor_ai.generate_vocab_card, level)
    await update.message.reply_text(vocab, parse_mode=ParseMode.MARKDOWN)

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=chat_id)
    level = db_user.get("level", "Intermediate")

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    quiz_data = await asyncio.to_thread(mentor_ai.generate_quiz, "English Grammar and Daily Usage", level)
    active_quizzes[chat_id] = quiz_data

    question_text = f"❓ **English Quiz ({level} Level):**\n\n{quiz_data.get('question', '')}\n\nসঠিক উত্তর নির্বাচন করুন:"
    options = quiz_data.get("options", [])

    keyboard = []
    for i, opt in enumerate(options):
        keyboard.append([InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"quiz_ans_{i}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(question_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def correct_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "⚠️ অনুগ্রহ করে সেন্টেন্স লিখুন।\nউদাহরণ: `/correct I am agree with your proposal.`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    sentence = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    analysis = await asyncio.to_thread(mentor_ai.analyze_sentence_deep, sentence)
    await update.message.reply_text(analysis, parse_mode=ParseMode.MARKDOWN)

async def setkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🔑 আপনার Gemini API Key সেট করতে লিখুন:\n`/setkey <your_gemini_api_key>`\n\nফ্রি কী পেতে যান: https://aistudio.google.com/",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    new_key = context.args[0].strip()
    config.GEMINI_API_KEY = new_key
    
    # Save to .env
    env_path = "/Users/sakibhossain/Workspace/08_Resources/ English Learning/.env"
    try:
        lines = []
        with open(env_path, "r") as f:
            lines = f.readlines()
        
        has_gemini = False
        new_lines = []
        for line in lines:
            if line.startswith("GEMINI_API_KEY="):
                new_lines.append(f"GEMINI_API_KEY={new_key}\n")
                has_gemini = True
            else:
                new_lines.append(line)
        if not has_gemini:
            new_lines.append(f"GEMINI_API_KEY={new_key}\n")
            
        with open(env_path, "w") as f:
            f.writelines(new_lines)
            
        await update.message.reply_text(
            "🎉 **Gemini API Key সফলভাবে যুক্ত হয়েছে!**\n\nএখন থেকে আপনার AI English Tutor পুরোদমে সক্রিয়। যেকোনো কিছু ইংরেজিতে লিখে প্র্যাকটিস শুরু করুন! 🚀",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Key সংরক্ষণ করতে সমস্যা হয়েছে: {e}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db_user = database.get_or_create_user(user_id=user_id, chat_id=update.effective_chat.id)
    vocab_count = database.get_user_vocab_count(user_id)
    mistakes_count = database.get_user_mistakes_count(user_id)

    stats_text = (
        f"📊 **আপনার লার্নিং প্রোফাইল:**\n\n"
        f"👤 **নাম:** {db_user.get('first_name')}\n"
        f"🔥 **বর্তমান স্ট্রিক:** {db_user.get('streak', 1)} দিন\n"
        f"🎯 **লেভেল:** {db_user.get('level', 'Intermediate')}\n"
        f"⚙️ **টিউটরিং মোড:** {db_user.get('mode', 'Tutor')}\n"
        f"📚 **সংরক্ষিত শব্দাবলী:** {vocab_count} টি\n"
        f"📝 **সংশোধিত ভুল:** {mistakes_count} টি\n"
        f"⏰ **প্রতিদিনের লেসন:** চালু আছে (সকাল ৯টা ও রাত ৮টা)\n\n"
        f"কীপ ইট আপ! প্রতিদিন অল্প একটু প্র্যাকটিসই আপনাকে সাবলীল করে তুলবে। 💪"
    )
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

async def mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🎓 Tutor (কথোপকথন + ভুল সংশোধন)", callback_data="set_mode_Tutor"),
        ],
        [
            InlineKeyboardButton("🧐 Strict (কঠোর ব্যাকরণ বিশ্লেষণ)", callback_data="set_mode_Strict"),
        ],
        [
            InlineKeyboardButton("☕ Casual (বন্ধুর মতো কথপোকথন)", callback_data="set_mode_Conversational"),
        ],
        [
            InlineKeyboardButton("💼 Business / Tech (অফিসিয়াল ও ক্লায়েন্ট কমিউনিকেশন)", callback_data="set_mode_Business"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 **আপনার পছন্দের টিউটরিং মোড বেছে নিন:**", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def level_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🌱 Beginner (প্রাথমিক)", callback_data="set_level_Beginner"),
            InlineKeyboardButton("🌿 Intermediate (মধ্যম)", callback_data="set_level_Intermediate"),
        ],
        [
            InlineKeyboardButton("🌳 Advanced (উন্নত)", callback_data="set_level_Advanced"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 **আপনার ইংরেজি দক্ষতার স্তর নির্বাচন করুন:**", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database.clear_chat_history(update.effective_user.id)
    await update.message.reply_text("🧹 আগের কথোপকথনের মেমোরি ক্লিয়ার করা হয়েছে! চলুন নতুন বিষয় নিয়ে আলোচনা শুরু করি।", parse_mode=ParseMode.MARKDOWN)

async def skills_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🎙️ 1. Pronunciation & Accent", callback_data="show_skill_pron"),
            InlineKeyboardButton("💼 2. Freelance Client Playbook", callback_data="show_skill_client"),
        ],
        [
            InlineKeyboardButton("⚡ 3. Native Slangs & Shortcuts", callback_data="show_skill_slang"),
            InlineKeyboardButton("🎓 4. IELTS & Exam Speaking", callback_data="show_skill_ielts"),
        ],
        [
            InlineKeyboardButton("📝 5. Real Grammar Patterns", callback_data="show_skill_grammar"),
            InlineKeyboardButton("📊 6. Technical Analytics English", callback_data="show_skill_tech"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    intro = (
        "📚 **English Mastery Skills Catalog (৬টি বিশেষায়িত লার্নিং স্কিল):**\n\n"
        "আপনার ইংরেজি শেখাকে আন্তর্জাতিক মানে নিয়ে যাওয়ার জন্য ৬টি পাওয়ারফুল স্কিল মডিউল প্রস্তুত করা হয়েছে:\n\n"
        "1. 🎙️ **Pronunciation & Accent Coach:** IPA, Flap-T, /w/ vs /v/, /th/ সাউন্ড ও রিদম\n"
        "2. 💼 **Freelance Client English:** আপওয়ার্ক বিডিং, জুম কল নেগোসিয়েশন ও $60/hr রেট বাড়ানো\n"
        "3. ⚡ **Native Slangs & Contractions:** ৩০০+ আমেরিকান ও ব্রিটিশ বাস্তব জীবনের স্ল্যাং ও শর্টকাট\n"
        "4. 🎓 **IELTS Speaking Band 8+:** AREA ও PPF মেথড দিয়ে ব্যান্ড ৭.৫-৮.৫ পাওয়ার কৌশল\n"
        "5. 📝 **Grammar in Real Life:** মুখস্থ ছাড়া বাস্তব জীবনে ১২টি টেন্স ও কন্ডিশনাল বাক্যের ব্যবহার\n"
        "6. 📊 **Technical Tracking Presenter:** GTM, GA4, CAPI ও সার্ভার ট্র্যাকিং মুখে বোঝানোর স্ক্রিপ্ট\n\n"
        "👉 নিচের বাটন থেকে যেকোনো একটি স্কিল সিলেক্ট করুন:"
    )
    await update.message.reply_text(intro, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def proposal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text(
            "💼 **Upwork Winning Proposal Generator:**\n\n"
            "বায়ারের জব পোস্ট পেস্ট করুন। যেমন:\n"
            "`/proposal We need an expert to fix Meta CAPI deduplication and GA4 server side tracking on Stape.io`\n\n"
            "আমি বায়ারের দেশ (USA/UK/AU) এবং সাইকোলজি বুঝে পারফেক্ট প্রপোজাল সাজিয়ে দেব।",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    job_text = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await update.message.reply_text("🧠 বায়ারের সাইকোলজি ও টেকনিক্যাল রিকোয়ারমেন্ট অ্যানালাইজ করা হচ্ছে, অনুগ্রহ করে কয়েক সেকেন্ড অপেক্ষা করুন...")
    
    proposal = await asyncio.to_thread(mentor_ai.generate_upwork_proposal, job_text)
    try:
        await update.message.reply_text(proposal, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning(f"Markdown proposal failed: {e}")
        await update.message.reply_text(proposal)

async def callhelp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text(
            "🚨 **Live Client Call Emergency Lifeline:**\n\n"
            "বায়ার জুমে বা কলে যা জিজ্ঞেস করেছে তা লিখুন। যেমন:\n"
            "`/callhelp Why are our purchase conversion values not matching between Shopify and GA4?`\n\n"
            "আমি সাথে সাথে মুখে বলার মতো ফ্লুয়েন্ট স্পিচ স্ক্রিপ্ট ও অডিও ভয়েস নোট পাঠিয়ে দেব!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    buyer_q = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    
    result = await asyncio.to_thread(mentor_ai.generate_call_lifeline, buyer_q)
    spoken_script = result.get("spoken_script", "")
    follow_up = result.get("follow_up", "")
    bangla_tip = result.get("bangla_tip", "")
    tts_text = result.get("tts_text", spoken_script)

    card = (
        f"🎙️ **Spoken Native Script (বায়ারকে মুখে যা বলবেন):**\n"
        f"*{spoken_script}*\n\n"
        f"💬 **Follow-up Question (কথোপকথন নিজের নিয়ন্ত্রণে রাখতে):**\n"
        f"*{follow_up}*\n\n"
        f"💡 **সাইকোলজিক্যাল টিপস:**\n{bangla_tip}"
    )
    try:
        await update.message.reply_text(card, parse_mode=ParseMode.MARKDOWN)
    except Exception:
        await update.message.reply_text(card)

    db_user = database.get_or_create_user(user_id=user_id, chat_id=chat_id)
    accent = db_user.get("accent", "US")
    voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")
    audio_bytes = await tts_service.text_to_speech_bytes(tts_text, voice=voice)
    if audio_bytes:
        try:
            await context.bot.send_voice(chat_id=chat_id, voice=audio_bytes)
        except Exception as e:
            logger.error(f"Callhelp audio failed: {e}")

async def screenexplain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 **Technical Screenshot Explainer:**\n\n"
        "যেকোনো GA4, GTM, Meta Events Manager, BigQuery বা ট্র্যাকিং ড্যাশবোর্ডের স্ক্রিনশট আমাকে সরাসরি পাঠান (ছবি পাঠানোর সময় ক্যাপশনে কিছু লিখতে পারেন বা শুধু ছবি পাঠালেও হবে)।\n\n"
        "বট স্ক্রিনশটের এরর/মেট্রিক দেখে বায়ারকে জুম কলে বা চ্যাটে মুখে কীভাবে সহজ ইংরেজিতে বুঝিয়ে বলবেন তার সুন্দর টেক্সট ও সমাধান সাজিয়ে দেবে!",
        parse_mode=ParseMode.MARKDOWN
    )

async def phonetics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🎯 **Phonetics & Accent Audit System:**\n\n"
        "বাঙালি ইংরেজি শিক্ষার্থীদের ক্ষেত্রে সবচেয়ে বেশি যে ৫টি উচ্চারণ অভ্যাস লক্ষ্য করা যায়:\n"
        "1. **/w/ vs /v/:** 'water' কে 'vater' বা 'very' কে 'wery' বলা।\n"
        "2. **/th/ Sound:** 'think' বা 'this' উচ্চারণ করার সময় দাঁতের সাথে জিহ্বা স্পর্শ না করা।\n"
        "3. **/r/ Rhoticity:** আমেরিকান রোবোটিক কার্ল ও ব্রিটিশ নন-রোটিক উচ্চারণ।\n"
        "4. **Dropped Endings:** শব্দের শেষের -ed, -s, -t উচ্চারণ বাদ পড়ে যাওয়া।\n"
        "5. **Speech Rhythm:** স্ট্রেস-টাইমড ন্যাচারাল রিদম।\n\n"
        "🎙️ **উচ্চারণ অডিট করতে:**\n"
        "যেকোনো ইংরেজি বাক্য মুখে পড়ে আমাকে একটি **ভয়েস মেসেজ (Voice Note)** পাঠান। আমি আপনার অডিও স্ক্যান করে অ্যাকসেন্ট হিটম্যাপ ও টিপস দিয়ে দেব!"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def scenario_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💰 $30 to $60/hr Rate Negotiation", callback_data="start_scen_rate"),
        ],
        [
            InlineKeyboardButton("😡 Angry Client De-escalation", callback_data="start_scen_angry"),
        ],
        [
            InlineKeyboardButton("☕ Zoom Pre-Meeting Small Talk", callback_data="start_scen_smalltalk"),
        ],
        [
            InlineKeyboardButton("🛑 Scope Creep Defense (Unpaid Work)", callback_data="start_scen_scope"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    intro = (
        "🎭 **Real-World Client Negotiation Simulator:**\n\n"
        "বাস্তব জীবনের কঠিন পরিস্থিতিগুলোতে আমেরিকান ক্লায়েন্টদের সাথে কীভাবে কনফিডেন্টলি এবং ডিপ্লোম্যাটিক্যালি কথা বলতে হয় তা প্র্যাকটিস করুন।\n\n"
        "কোন পরিস্থিতিটি সিমুলেট করতে চান নির্বাচন করুন:"
    )
    await update.message.reply_text(intro, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def endscenario_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current = database.get_scenario_state(user_id)
    if not current:
        await update.message.reply_text("বর্তমানে কোনো অ্যাক্টিভ সিনারিও সিমুলেশন চালু নেই। নতুন সিনারিও শুরু করতে `/scenario` লিখুন।")
        return
    database.set_scenario_state(user_id, "")
    await update.message.reply_text("🏁 **সিনারিও সিমুলেশন শেষ হয়েছে!**\n\nআপনি স্বাভাবিক টিউটর মোডে ফিরে এসেছেন। আবার শুরু করতে `/scenario` লিখুন।", parse_mode=ParseMode.MARKDOWN)

async def srs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    due_items = database.get_due_srs_items(user_id, limit=1)

    if not due_items:
        srs_data = {
            "id": 0,
            "prompt": "What is the native meaning of 'touch base'?",
            "correct": "To briefly make contact or talk to someone",
            "options": [
                "To briefly make contact or talk to someone",
                "To play baseball in the park",
                "To finish the entire project today",
                "To blame someone for an error"
            ],
            "explanation": "'Touch base' হলো একটি অত্যন্ত বহুল ব্যবহৃত আমেরিকান কর্পোরেট/ক্লায়েন্ট স্ল্যাং, যার অর্থ সংক্ষিপ্তভাবে খোঁজ নেওয়া বা আপডেট দেওয়া।"
        }
    else:
        item = due_items[0]
        srs_data = {
            "id": item["id"],
            "prompt": item["prompt"],
            "correct": item["correct_answer"],
            "options": item.get("options", []),
            "explanation": item.get("explanation", "")
        }

    question_text = (
        f"🧠 **Spaced Repetition Flashcard (Ebbinghaus System):**\n\n"
        f"*{srs_data['prompt']}*\n\n"
        f"সঠিক উত্তর বেছে নিন:"
    )
    keyboard = []
    options = srs_data["options"]
    correct_ans = srs_data["correct"]
    for i, opt in enumerate(options):
        is_correct = "1" if opt == correct_ans else "0"
        cb_id = srs_data.get("id", 0)
        keyboard.append([InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"srs_ans_{cb_id}_{is_correct}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(question_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = (
        "🚀 **Antigravity English Web Studio & Live Voice Caller:**\n\n"
        "আপনার কাস্টম ডোমেইন ড্যাশবোর্ড ও ইন্টারঅ্যাক্টিভ অডিও স্টুডিও সরাসরি ভিজিট করুন:\n"
        "👉 **[tutor.sakibhossain.io](https://tutor.sakibhossain.io)**\n"
        "👉 **[tutor.sakibhossain.online](https://tutor.sakibhossain.online)**\n\n"
        "✨ **ফিচারসমূহ:**\n"
        "• 🎙️ Web Voice Caller (লাইভ অডিও কথা বলা)\n"
        "• 📊 স্ট্রিক ও ফ্লুয়েন্সি স্কোরকার্ড\n"
        "• 💼 ফ্রিল্যান্সিং ও আপওয়ার্ক চিটশিট\n"
        "• 🗂️ ফ্ল্যাশ কার্ড ওয়ার্ড ব্যাংক"
    )
    keyboard = [
        [
            InlineKeyboardButton("🌐 Open Web Studio", url="https://tutor.sakibhossain.io"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(card, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if data.startswith("set_level_"):
        new_level = data.replace("set_level_", "")
        database.update_user_level(user_id, new_level)
        await query.edit_message_text(
            f"✅ আপনার লেভেল সফলভাবে **{new_level}** হিসেবে সেট করা হয়েছে!\n\nএখন যেকোনো কিছু ইংরেজিতে লিখে পাঠান, আমি আপনার সাথে চ্যাট করব এবং প্রয়োজনে ভুল ঠিক করে দিব।",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("set_mode_"):
        new_mode = data.replace("set_mode_", "")
        database.update_user_mode(user_id, new_mode)
        await query.edit_message_text(
            f"✅ আপনার টিউটরিং মোড পরিবর্তিত হয়েছে: **{new_mode}**!\n\nনতুন মোডে প্র্যাকটিস করতে এখনই কোনো প্রশ্ন বা বাক্য লিখুন।",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("set_accent_"):
        new_accent = data.replace("set_accent_", "")
        database.update_user_accent(user_id, new_accent)
        accent_names = {"US": "American (USA)", "UK": "British (UK)", "AUS": "Australian"}
        await query.edit_message_text(
            f"✅ আপনার পছন্দের অ্যাকসেন্ট **{accent_names.get(new_accent, new_accent)}** সফলভাবে সেট করা হয়েছে!\n\nএখন থেকে অডিও ভয়েস মেসেজ এই অ্যাকসেন্টে পাঠানো হবে।",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("start_interview_"):
        scen_type = data.replace("start_interview_", "")
        scenarios = {
            "client": "Upwork Freelance Client Call for a Tracking / Web Analytics Project",
            "tech": "Technical Job Interview for an Analytics / Developer role",
            "visa": "US/UK Visa & Immigration Officer Interview"
        }
        scenario_desc = scenarios.get(scen_type, "Client Interview")
        database.set_interview_state(user_id, scenario_desc)

        first_question = {
            "client": "Hey there! Thanks for hopping on the call. I saw your proposal for our analytics tracking setup. Could you give me a quick rundown of your experience and what you've worked on recently?",
            "tech": "Hello! Welcome to the interview. To kick things off, could you introduce yourself and tell me about a challenging project you handled recently?",
            "visa": "Good morning. Please state the primary purpose of your trip and how long you intend to stay."
        }.get(scen_type, "Hello! Could you please introduce yourself?")

        database.add_chat_history(user_id, "model", first_question)

        db_user = database.get_or_create_user(user_id=user_id, chat_id=chat_id)
        accent = db_user.get("accent", "US")
        voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")
        audio_bytes = await tts_service.text_to_speech_bytes(first_question, voice=voice)

        await query.edit_message_text(
            f"🎬 **ইন্টারভিউ শুরু হয়েছে! ({scenario_desc})**\n\n"
            f"👤 **Interviewer:**\n*\"{first_question}\"*\n\n"
            f"👉 আপনি টেক্সট লিখে অথবা **ভয়েস মেসেজ পাঠিয়ে** উত্তর দিন।\n"
            f"(ইন্টারভিউ শেষ করতে লিখবেন: `/endinterview`)",
            parse_mode=ParseMode.MARKDOWN
        )
        if audio_bytes:
            try:
                await context.bot.send_voice(chat_id=chat_id, voice=audio_bytes)
            except Exception as e:
                logger.error(f"Interview voice send failed: {e}")

    elif data.startswith("quiz_ans_"):
        selected_index = int(data.replace("quiz_ans_", ""))
        quiz = active_quizzes.get(chat_id)
        if not quiz:
            await query.edit_message_text("⌛ কুইজের সময় শেষ হয়ে গিয়েছে বা নতুন কুইজ শুরু করা হয়েছে। `/quiz` দিন।")
            return

        correct_index = quiz.get("correct_index", 0)
        explanation = quiz.get("explanation", "")
        options = quiz.get("options", [])
        question = quiz.get("question", "")

        is_correct = (selected_index == correct_index)
        result_icon = "🎉 **সঠিক উত্তর! (Correct!)**" if is_correct else "❌ **ভুল উত্তর! (Incorrect)**"
        correct_answer_text = options[correct_index] if 0 <= correct_index < len(options) else ""

        response_msg = (
            f"❓ {question}\n\n"
            f"{result_icon}\n"
            f"📌 **সঠিক উত্তর:** {chr(65+correct_index)}. {correct_answer_text}\n\n"
            f"💡 **ব্যাখ্যা:**\n{explanation}\n\n"
            f"পরের কুইজের জন্য `/quiz` লিখুন!"
        )
        # Clean up
        active_quizzes.pop(chat_id, None)
        await query.edit_message_text(response_msg, parse_mode=ParseMode.MARKDOWN)

    elif data.startswith("start_scen_"):
        scen_type = data.replace("start_scen_", "")
        database.set_scenario_state(user_id, scen_type)

        scen_titles = {
            "rate": "💰 $30 to $60/hr Rate Negotiation",
            "angry": "😡 Angry Client De-escalation",
            "smalltalk": "☕ Pre-Meeting Small Talk",
            "scope": "🛑 Scope Creep Defense"
        }
        openings = {
            "rate": "Hey Sakib, we really appreciate your work on our Google Tag Manager container. But honestly, bumping the rate from $30 up to $60 an hour is a big jump for our quarterly budget. How do you justify doubling the cost?",
            "angry": "Sakib, what happened to our Facebook campaigns?! Our reported purchase conversions plummeted by 40% over the weekend right after you touched the tags! We're burning money on ads!",
            "smalltalk": "Hey Sakib! Good to see you on the call. Man, it has been pouring down rain here in Chicago all morning! How are things on your end today?",
            "scope": "Hey, by the way, since you're already in our GTM container fixing GA4, could you also quickly set up tracking on our other 4 subdomain stores and connect them to our ActiveCampaign CRM?"
        }

        opening_text = openings.get(scen_type, "Hey, thanks for joining. Let's discuss the project.")
        database.add_chat_history(user_id, "model", opening_text)

        db_user = database.get_or_create_user(user_id=user_id, chat_id=chat_id)
        accent = db_user.get("accent", "US")
        voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")
        audio_bytes = await tts_service.text_to_speech_bytes(opening_text, voice=voice)

        await query.edit_message_text(
            f"🎬 **সিনারিও সিমুলেশন শুরু হয়েছে!**\n"
            f"*{scen_titles.get(scen_type, 'Negotiation')}*\n\n"
            f"👤 **Client:**\n*\"{opening_text}\"*\n\n"
            f"👉 আপনি টেক্সট লিখে অথবা **ভয়েস মেসেজে** ক্লায়েন্টকে উত্তর দিন।\n"
            f"(সিনারিও বন্ধ করতে লিখবেন: `/endscenario`)",
            parse_mode=ParseMode.MARKDOWN
        )
        if audio_bytes:
            try:
                await context.bot.send_voice(chat_id=chat_id, voice=audio_bytes)
            except Exception as e:
                logger.error(f"Scenario opening voice failed: {e}")

    elif data.startswith("srs_ans_"):
        parts = data.replace("srs_ans_", "").split("_")
        item_id = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        is_correct = (parts[1] == "1") if len(parts) > 1 else False

        if item_id > 0:
            database.update_srs_item_result(item_id, is_correct)

        if is_correct:
            res_text = (
                "🎉 **Brilliant! একদম সঠিক উত্তর!**\n\n"
                "🧠 **Ebbinghaus SRS Progress:**\n"
                "আপনার মেমোরি ইন্টারভ্যাল পরবর্তী স্টেজে উন্নীত হয়েছে (+৩/৭ দিন পর আবার রিভিজিট করা হবে)।\n\n"
                "পরবর্তী ফ্ল্যাশ কার্ডের জন্য `/srs` লিখুন।"
            )
        else:
            res_text = (
                "❌ **Oops! উত্তরটি সঠিক হয়নি।**\n\n"
                "💡 **টিপস:** কোনো সমস্যা নেই! Ebbinghaus মেমোরি অ্যালগরিদম অনুযায়ী এই শব্দটি কাল আবার আপনার সামনে আনা হবে যাতে স্থায়ীভাবে মাথায় গেঁথে যায়।\n\n"
                "পরবর্তী ফ্ল্যাশ কার্ডের জন্য `/srs` লিখুন।"
            )
        await query.edit_message_text(res_text, parse_mode=ParseMode.MARKDOWN)

    elif data.startswith("show_skill_"):
        sk = data.replace("show_skill_", "")
        skill_cards = {
            "pron": (
                "🎙️ **Skill 1: Pronunciation & Accent Coach**\n\n"
                "• **American Flap-T:** 'water' -> 'wader', 'city' -> 'cidy'\n"
                "• **Glottal Stop:** 'button' -> 'bu-n', 'important' -> 'impor-nt'\n"
                "• **/w/ vs /v/:** ঠোঁট গোল করে বাঁশির মতো ফুঁ দিয়ে 'water' বলুন।\n"
                "• **/th/ Sound:** জিহ্বার ডগা ওপর-নিচের দাঁতের মাঝে চেপে হালকা বাতাস ছাড়ুন ('think', 'this')।\n\n"
                "👉 উচ্চারণ টেস্ট করতে একটি ইংরেজি ভয়েস নোট পাঠান!"
            ),
            "client": (
                "💼 **Skill 2: Freelance Client English Playbook**\n\n"
                "• **উইনিং প্রপোজাল:** প্রথম ২ লাইনে বায়ারের টেকনিক্যাল সমস্যা বলুন।\n"
                "• **$60/hr রেট বাড়ানো:** বায়ারের লাভ ও অ্যাড স্পেন্ড লস রিকভারির যুক্তি দিন।\n"
                "• **জরুরি কল হেল্প:** বায়ারকে বলুন *'Let me pull up Tag Assistant to verify the payload.'*\n\n"
                "👉 প্রপোজাল বানাতে লিখুন: `/proposal <জব পোস্ট>`"
            ),
            "slang": (
                "⚡ **Skill 3: Native Slangs & Contractions**\n\n"
                "• **Gonna / Wanna / Gotta:** Going to / Want to / Have got to\n"
                "• **I'm beat:** খুব ক্লান্ত\n"
                "• **Touch base:** সংক্ষেপে আপডেট নেওয়া\n"
                "• **Ballpark:** আনুমানিক হিসাব\n"
                "• **No sweat:** কোনো ব্যাপারই না\n\n"
                "👉 যেকোনো স্ল্যাং ডিকোড করতে লিখুন: `/decode <স্ল্যাং>`"
            ),
            "ielts": (
                "🎓 **Skill 4: IELTS & Exam Speaking Band 8+**\n\n"
                "• **AREA Method:** Answer + Reason + Example + Alternative\n"
                "• **PPF Method (Part 2 Cue Card):** Past (শুরু) + Present (সমাধান) + Future (ভবিষ্যৎ শিক্ষা)\n"
                "• **Band 8 Signposts:** *'On balance, I'm inclined to believe...'* / *'It's a double-edged sword...'* \n\n"
                "👉 লাইভ ইন্টারভিউ প্র্যাকটিস করতে লিখুন: `/interview`"
            ),
            "grammar": (
                "📝 **Skill 5: Real-World Grammar Patterns**\n\n"
                "• **Past Simple vs Present Perfect:** সময় শেষ হলে Past Simple ('fixed yesterday'), ফল এখনও কার্যকর হলে Present Perfect ('have fixed').\n"
                "• **Diplomatic 2nd Conditional:** *'If we updated the container, it would take 5 hours.'*\n"
                "• **Preposition Magic:** AT 9:00 AM, ON Monday, IN November.\n\n"
                "👉 বাক্য চেক করতে লিখুন: `/correct <বাক্য>`"
            ),
            "tech": (
                "📊 **Skill 6: Technical Tracking Presenter**\n\n"
                "• **Deduplication:** *'Preventing double counting via browser and server event_id matching.'*\n"
                "• **Server-Side Pitch:** *'Bypasses ad blockers and recovers 20-25% lost conversions.'*\n"
                "• **EMQ Score 8+:** *'Passing normalized SHA-256 hashed customer parameters.'*\n\n"
                "👉 স্ক্রিনশট বুঝিয়ে বলতে পাঠান ছবি বা লিখুন: `/screenexplain`"
            )
        }
        text = skill_cards.get(sk, "স্কিল মডিউল লোড করা হয়েছে।")
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()

    # Get user profile
    db_user = database.get_or_create_user(
        user_id=user.id,
        chat_id=chat_id,
        username=user.username or "",
        first_name=user.first_name or "Friend"
    )

    level = db_user.get("level", "Intermediate")
    mode = db_user.get("mode", "Tutor")

    # Send typing indicator
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Auto-detect YouTube links in regular chat
    if "youtube.com" in user_text or "youtu.be" in user_text:
        await update.message.reply_text("🎬 YouTube লিংক শনাক্ত হয়েছে! ট্রান্সক্রিপ্ট সংগ্রহ ও বিশ্লেষণ করা হচ্ছে, অনুগ্রহ করে কয়েক সেকেন্ড অপেক্ষা করুন...")
        yt_reply = await asyncio.to_thread(mentor_ai.analyze_youtube_transcript, user_text, level)
        try:
            await update.message.reply_text(yt_reply, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.warning(f"Markdown send failed on YT reply: {e}")
            await update.message.reply_text(yt_reply)
        return

    # Fetch history
    history = database.get_chat_history(user.id, limit=8)

    # Save user message to DB
    database.add_chat_history(user.id, "user", user_text)

    # Check for active interview simulator
    active_interview = database.get_interview_state(user.id)
    if active_interview:
        reply = await asyncio.to_thread(
            mentor_ai.generate_interview_turn,
            scenario=active_interview,
            history=history,
            user_reply=user_text
        )
        database.add_chat_history(user.id, "model", reply)
        try:
            await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.warning(f"Markdown send failed on interview reply: {e}")
            await update.message.reply_text(reply)

        accent = db_user.get("accent", "US")
        voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")
        audio_bytes = await tts_service.text_to_speech_bytes(reply, voice=voice)
        if audio_bytes:
            try:
                await context.bot.send_voice(chat_id=chat_id, voice=audio_bytes)
            except Exception as e:
                logger.error(f"Voice send failed: {e}")
        return

    # Check for active negotiation scenario
    active_scenario = database.get_scenario_state(user.id)
    if active_scenario:
        scenario_result = await asyncio.to_thread(
            mentor_ai.simulate_scenario_turn,
            scenario_type=active_scenario,
            history=history,
            user_reply=user_text
        )
        client_reply = scenario_result.get("client_reply", "")
        score = scenario_result.get("user_performance_score", 8)
        feedback = scenario_result.get("diplomacy_feedback", "")
        rec_saying = scenario_result.get("recommended_next_saying", "")
        tip_bn = scenario_result.get("tip_bn", "")

        msg = (
            f"👤 **Client Reaction:**\n*\"{client_reply}\"*\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **Performance Score:** {score}/10\n"
            f"🔍 **Diplomacy & Tone:** {feedback}\n"
            f"💡 **Better Native Phrasing:** *\"{rec_saying}\"*\n"
            f"🇧🇩 **কৌশলগত পরামর্শ:** {tip_bn}\n\n"
            f"👉 আপনি ক্লায়েন্টকে পরবর্তী জবাব দিন (বা শেষ করতে `/endscenario` লিখুন)।"
        )
        database.add_chat_history(user.id, "model", client_reply)
        try:
            await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text(msg)

        accent = db_user.get("accent", "US")
        voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")
        audio_bytes = await tts_service.text_to_speech_bytes(client_reply, voice=voice)
        if audio_bytes:
            try:
                await context.bot.send_voice(chat_id=chat_id, voice=audio_bytes)
            except Exception as e:
                logger.error(f"Voice send failed: {e}")
        return

    # Generate Tutor AI reply in background thread
    reply = await asyncio.to_thread(
        mentor_ai.generate_tutor_reply,
        user_message=user_text,
        history=history,
        user_level=level,
        user_mode=mode
    )

    # Save AI response to DB
    database.add_chat_history(user.id, "model", reply)

    # Reply to user
    try:
        await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        # Fallback if markdown parsing fails due to unescaped special chars
        logger.warning(f"Markdown send failed, falling back to plain text: {e}")
        await update.message.reply_text(reply)

    # Optional Native Voice Message
    if db_user.get("voice_enabled", 1):
        accent = db_user.get("accent", "US")
        voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")
        audio_bytes = await tts_service.text_to_speech_bytes(reply, voice=voice)
        if audio_bytes:
            try:
                await context.bot.send_voice(chat_id=chat_id, voice=audio_bytes)
            except Exception as e:
                logger.error(f"Voice send failed: {e}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.voice:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id

    # Send typing action
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        voice = update.message.voice
        voice_file = await context.bot.get_file(voice.file_id)
        audio_bytes = await voice_file.download_as_bytearray()
    except Exception as e:
        logger.error(f"Error downloading voice message: {e}")
        await update.message.reply_text("❌ ভয়েস মেসেজ ডাউনলোড করতে সমস্যা হয়েছে। দয়া করে আবার পাঠান।")
        return

    db_user = database.get_or_create_user(
        user_id=user.id,
        chat_id=chat_id,
        username=user.username or "",
        first_name=user.first_name or "Friend"
    )

    level = db_user.get("level", "Intermediate")
    mode = db_user.get("mode", "Native")

    reply = await asyncio.to_thread(
        mentor_ai.generate_voice_tutor_reply,
        audio_bytes=bytes(audio_bytes),
        history=database.get_chat_history(user.id, limit=6),
        user_level=level,
        user_mode=mode
    )

    # Phonetics and Accent Audit
    try:
        phonetics = await asyncio.to_thread(
            mentor_ai.analyze_phonetics_deep,
            audio_bytes=bytes(audio_bytes),
            mime_type="audio/ogg"
        )
        clarity = phonetics.get("clarity_score", 8)
        pb = phonetics.get("phonetic_breakdown", [])
        overall_bn = phonetics.get("overall_feedback_bn", "")
        phonetic_box = f"\n\n━━━━━━━━━━━━━━━━━━━\n🎯 **Phonetic & Accent Audit:** {clarity}/10\n"
        for item in pb[:2]:
            phonetic_box += f"• **{item.get('word')}** ({item.get('target_sound')}): {item.get('tip_bn')}\n"
        if overall_bn:
            phonetic_box += f"💡 {overall_bn}\n"
        reply += phonetic_box
    except Exception as e:
        logger.debug(f"Phonetic audit error: {e}")

    database.add_chat_history(user.id, "user", "[Voice Message]")
    database.add_chat_history(user.id, "model", reply)

    try:
        await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning(f"Markdown send failed on voice reply: {e}")
        await update.message.reply_text(reply)

    # Send Native Voice reply
    accent = db_user.get("accent", "US")
    voice = VOICE_MAP.get(accent, "en-US-ChristopherNeural")
    audio_reply_bytes = await tts_service.text_to_speech_bytes(reply, voice=voice)
    if audio_reply_bytes:
        try:
            await context.bot.send_voice(chat_id=chat_id, voice=audio_reply_bytes)
        except Exception as e:
            logger.error(f"Voice reply failed: {e}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id
    caption = update.message.caption or ""

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        photo = update.message.photo[-1]
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
    except Exception as e:
        logger.error(f"Error downloading photo: {e}")
        await update.message.reply_text("❌ ছবি ডাউনলোড করতে সমস্যা হয়েছে। দয়া করে আবার পাঠান।")
        return

    db_user = database.get_or_create_user(
        user_id=user.id,
        chat_id=chat_id,
        username=user.username or "",
        first_name=user.first_name or "Friend"
    )
    level = db_user.get("level", "Intermediate")

    lower_caption = caption.lower()
    is_screen_explain = any(k in lower_caption for k in [
        "/screenexplain", "screen", "explain", "client", "error", "gtm", "ga4", "capi", "buyer", "tag", "pixel", "metric", "dashboard"
    ])

    if is_screen_explain:
        reply = await asyncio.to_thread(
            mentor_ai.analyze_screen_explain,
            image_bytes=bytes(photo_bytes),
            mime_type="image/jpeg",
            caption=caption
        )
    else:
        reply = await asyncio.to_thread(
            mentor_ai.generate_image_tutor_reply,
            image_bytes=bytes(photo_bytes),
            caption=caption,
            user_level=level
        )

    try:
        await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning(f"Markdown send failed on photo reply: {e}")
        await update.message.reply_text(reply)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.video:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id
    caption = update.message.caption or ""
    video = update.message.video

    if video.file_size and video.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("⚠️ টেলিগ্রামের মাধ্যমে সর্বোচ্চ ২০ মেগাবাইট (20MB) পর্যন্ত ভিডিও পাঠানো সম্ভব। দয়া করে ছোট ভিডিও ক্লিপ পাঠান।")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    temp_video_path = f"/tmp/tutor_vid_{user.id}_{video.file_id[:10]}.mp4"
    try:
        video_file = await context.bot.get_file(video.file_id)
        await video_file.download_to_drive(temp_video_path)
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await update.message.reply_text("❌ ভিডিও ডাউনলোড করতে সমস্যা হয়েছে। দয়া করে আবার পাঠান।")
        return

    db_user = database.get_or_create_user(
        user_id=user.id,
        chat_id=chat_id,
        username=user.username or "",
        first_name=user.first_name or "Friend"
    )
    level = db_user.get("level", "Intermediate")

    reply = await asyncio.to_thread(
        mentor_ai.generate_video_tutor_reply,
        video_path=temp_video_path,
        caption=caption,
        user_level=level
    )

    if os.path.exists(temp_video_path):
        os.remove(temp_video_path)

    try:
        await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.warning(f"Markdown send failed on video reply: {e}")
        await update.message.reply_text(reply)

async def post_init(application):
    scheduler.setup_scheduler(application.bot)
    try:
        from telegram import MenuButtonWebApp, WebAppInfo
        await application.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🚀 Web Studio",
                web_app=WebAppInfo(url="https://tutor.sakibhossain.io")
            )
        )
        logger.info("Telegram Mini App menu button configured: https://tutor.sakibhossain.io")
    except Exception as e:
        logger.warning(f"Could not set web app menu button: {e}")
    logger.info("Background scheduler initialized in post_init.")

def main():
    database.init_db()

    is_valid, msg = config.validate_config()
    if not is_valid:
        print(f"\n❌ Configuration Error: {msg}")
        return

    print("🚀 Starting Antigravity English Mentor Telegram Bot...")
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).post_init(post_init).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("decode", decode_command))
    app.add_handler(CommandHandler("bn", bn_command))
    app.add_handler(CommandHandler("shadow", shadow_command))
    app.add_handler(CommandHandler("interview", interview_command))
    app.add_handler(CommandHandler("endinterview", endinterview_command))
    app.add_handler(CommandHandler("review", review_command))
    app.add_handler(CommandHandler("yt", youtube_command))
    app.add_handler(CommandHandler("youtube", youtube_command))
    app.add_handler(CommandHandler("client", client_command))
    app.add_handler(CommandHandler("speak", speak_command))
    app.add_handler(CommandHandler("listen", listen_command))
    app.add_handler(CommandHandler("accent", accent_command))
    app.add_handler(CommandHandler("voice", voice_command))
    app.add_handler(CommandHandler("lesson", lesson_command))
    app.add_handler(CommandHandler("vocab", vocab_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CommandHandler("correct", correct_command))
    app.add_handler(CommandHandler("setkey", setkey_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("mode", mode_command))
    app.add_handler(CommandHandler("level", level_command))
    app.add_handler(CommandHandler("clear", clear_command))

    # New Superpowers
    app.add_handler(CommandHandler("proposal", proposal_command))
    app.add_handler(CommandHandler("callhelp", callhelp_command))
    app.add_handler(CommandHandler("screenexplain", screenexplain_command))
    app.add_handler(CommandHandler("phonetics", phonetics_command))
    app.add_handler(CommandHandler("scenario", scenario_command))
    app.add_handler(CommandHandler("endscenario", endscenario_command))
    app.add_handler(CommandHandler("srs", srs_command))
    app.add_handler(CommandHandler("app", app_command))
    app.add_handler(CommandHandler("skills", skills_command))

    # Callback queries (Buttons)
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    # Regular text messages
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Voice & Audio messages
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))

    # Photos & Images
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Videos
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    # Documents & PDFs
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("✅ Bot is running! Listening for Telegram messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
