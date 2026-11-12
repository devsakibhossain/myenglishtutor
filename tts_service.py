import io
import re
import edge_tts
import logging

logger = logging.getLogger(__name__)

DEFAULT_VOICE = "en-US-ChristopherNeural"

def extract_spoken_text(full_reply: str) -> str:
    """Extracts only the English conversational part for audio, skipping the markdown decoder boxes."""
    # Split by common separator or take the first 1-3 sentences before the decoder box
    clean = full_reply
    if "🎧" in clean:
        clean = clean.split("🎧")[0]
    if "🔍" in clean:
        clean = clean.split("🔍")[0]
    if "📝" in clean:
        clean = clean.split("📝")[0]
    if "---" in clean:
        clean = clean.split("---")[0]
        
    # Remove markdown asterisks, hashes
    clean = re.sub(r"[\*\_#`]", "", clean).strip()
    # Limit length so audio is concise (1-2 sentences)
    sentences = [s.strip() for s in clean.split(".") if s.strip()]
    if sentences:
        return ". ".join(sentences[:3]) + "."
    return clean[:200]

async def text_to_speech_bytes(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    """Generates audio bytes using Edge TTS neural voice."""
    try:
        spoken = extract_spoken_text(text)
        if not spoken:
            spoken = text[:150]
        communicate = edge_tts.Communicate(spoken, voice=voice)
        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        audio_stream.seek(0)
        return audio_stream.read()
    except Exception as e:
        logger.error(f"TTS generation error: {e}")
        return b""
