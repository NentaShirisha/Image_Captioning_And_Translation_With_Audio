from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from deep_translator import GoogleTranslator
from gtts import gTTS
import torch
import uuid
import os

processor = None
model = None

def get_processor():
    global processor
    if processor is None:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor

def get_model():
    global model
    if model is None:
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return model

def generate_caption(image_path):
    try:
        print(f"Processing image: {image_path}")
        raw_image = Image.open(image_path).convert("RGB")
        inputs = get_processor()(raw_image, return_tensors="pt")
        out = get_model().generate(**inputs)
        caption = get_processor().decode(out[0], skip_special_tokens=True)
        print(f"Generated caption: {caption}")
        return caption
    except Exception as e:
        print(f"Error generating caption: {e}")
        return f"Error generating caption: {str(e)}"

def translate_text(text, language):
    try:
        print(f"Translating '{text}' to {language}")
        result = GoogleTranslator(source='auto', target=language).translate(text)
        print(f"Translation result: {result}")
        return result
    except Exception as e:
        print(f"Error translating: {e}")
        return text  # Return original text if translation fails

def text_to_speech(text, language='en'):
    try:
        print(f"Generating speech for: '{text}' in {language}")
        filename = f"audio_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang=language)
        filepath = os.path.join('media', 'audio', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        tts.save(filepath)
        print(f"Audio saved to: {filepath}")
        return f"audio/{filename}"
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None