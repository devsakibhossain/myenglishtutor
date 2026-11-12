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
