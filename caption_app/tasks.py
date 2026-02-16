from celery import shared_task
from .ai_engine import generate_caption, translate_text, text_to_speech
from .models import CaptionHistory
import os

@shared_task
def process_caption(image_path, language, user_id):
    # Generate caption
    caption = generate_caption(image_path)
    
    # Translate
    translated = translate_text(caption, language)
    
    # Generate audio
    audio_path = text_to_speech(translated, language)
    
    # Save to database
    history = CaptionHistory.objects.create(
        user_id=user_id,
        image=image_path,
        caption=caption,
        language=language,
        translated_text=translated,
        audio_file=audio_path
    )
    
    return {
        'caption': caption,
        'translation': translated,
        'audio_url': audio_path
    }