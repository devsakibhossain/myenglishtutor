import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import database
import mentor_ai

logger = logging.getLogger(__name__)

async def send_daily_morning_lesson(bot):
    """Sends morning bite/lesson to all active subscribers."""
    logger.info("Executing daily morning lesson job...")
    subscribers = database.get_all_subscribers()
    for user in subscribers:
        chat_id = user["chat_id"]
        level = user.get("level", "Intermediate")
        first_name = user.get("first_name", "Friend")
        streak = user.get("streak", 1)

        try:
            lesson_text = mentor_ai.generate_daily_lesson(level)
            header = (
                f"🌅 **Good morning, {first_name}!**\n"
                f"🔥 **Your Streak:** {streak} Days in a row!\n\n"
                f"Here is your English Lesson for today:\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
            )
            message = header + lesson_text
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            logger.info(f"Morning lesson delivered to chat_id={chat_id}")
        except Exception as e:
            logger.error(f"Failed to send morning lesson to {chat_id}: {e}")

async def send_evening_vocab_quiz(bot):
    """Sends evening vocabulary challenge to all active subscribers."""
    logger.info("Executing daily evening vocabulary job...")
    subscribers = database.get_all_subscribers()
    for user in subscribers:
        chat_id = user["chat_id"]
        level = user.get("level", "Intermediate")

        try:
            vocab_text = mentor_ai.generate_vocab_card(level)
            header = (
                "🌙 **Evening Vocabulary Booster!**\n"
                "Take 2 minutes to learn this word before bed:\n"
                "━━━━━━━━━━━━━━━━━━━\n"
            )
            message = header + vocab_text
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            logger.info(f"Evening vocab delivered to chat_id={chat_id}")
        except Exception as e:
            logger.error(f"Failed to send evening vocab to {chat_id}: {e}")

async def send_daily_srs_quiz(bot):
    """Checks for due SRS review items (Ebbinghaus forgetting curve intervals) and sends interactive buttons."""
    logger.info("Executing daily SRS review job...")
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    subscribers = database.get_all_subscribers()
    for user in subscribers:
        user_id = user["user_id"]
        chat_id = user["chat_id"]
        due_items = database.get_due_srs_items(user_id, limit=1)
        if not due_items:
            continue
        item = due_items[0]
        prompt = item["prompt"]
        options = item.get("options", [])
        correct_ans = item["correct_answer"]
        item_id = item["id"]

        keyboard = []
        for i, opt in enumerate(options):
            is_correct = "1" if opt == correct_ans else "0"
            keyboard.append([InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"srs_ans_{item_id}_{is_correct}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = (
            f"🧠 **Spaced Repetition Review (স্মৃতি পরীক্ষা):**\n\n"
            f"*{prompt}*\n\n"
            f"সঠিক উত্তর বেছে নিন:"
        )
        try:
            await bot.send_message(chat_id=chat_id, text=msg, reply_markup=reply_markup, parse_mode="Markdown")
            logger.info(f"Daily SRS quiz sent to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send daily SRS quiz to {chat_id}: {e}")

def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # Morning lesson at 09:00 AM every day
    scheduler.add_job(
        send_daily_morning_lesson,
        CronTrigger(hour=9, minute=0),
        args=[bot],
        id="morning_lesson",
        replace_existing=True
    )

    # Afternoon Spaced Repetition (SRS) at 15:00 (3:00 PM) every day
    scheduler.add_job(
        send_daily_srs_quiz,
        CronTrigger(hour=15, minute=0),
        args=[bot],
        id="daily_srs",
        replace_existing=True
    )

    # Evening vocabulary at 20:00 (8:00 PM) every day
    scheduler.add_job(
        send_evening_vocab_quiz,
        CronTrigger(hour=20, minute=0),
        args=[bot],
        id="evening_vocab",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler initialized: Morning lessons (09:00) & Evening vocab (20:00).")
    return scheduler
