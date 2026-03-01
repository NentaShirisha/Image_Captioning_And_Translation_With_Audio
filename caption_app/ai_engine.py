from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from deep_translator import GoogleTranslator
from gtts import gTTS
import torch
import uuid
import os

processor = None
model = None

# Load processor lazily (Render safe)
def get_processor():
    global processor
    if processor is None:
        print("Loading BLIP Processor...")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor

# Load model lazily (CPU safe)
def get_model():
    global model
    if model is None:
        print("Loading BLIP Model...")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        model.eval()  # production safe
    return model

# -------------------------------
# SAFE CAPTION GENERATION
# -------------------------------
def generate_caption(image_path):
    try:
        print(f"Processing image: {image_path}")

        raw_image = Image.open(image_path).convert("RGB")

        processor = get_processor()
        model = get_model()

        # 🔴 VERY IMPORTANT FIX FOR RENDER CPU
        inputs = processor(
            images=raw_image,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=50,
                num_beams=4,
                early_stopping=True
            )

        caption = processor.decode(output[0], skip_special_tokens=True)

        print(f"Generated caption: {caption}")
        return caption

    except Exception as e:
        print(f"Error generating caption: {e}")
        return None


# -------------------------------
# SAFE TRANSLATION
# -------------------------------
def translate_text(text, language):
    try:
        if not text:
            return ""

        print(f"Translating '{text}' to {language}")
        result = GoogleTranslator(source='auto', target=language).translate(text)
        print(f"Translation result: {result}")
        return result

    except Exception as e:
        print(f"Error translating: {e}")
        return text


# -------------------------------
# SAFE AUDIO GENERATION
# -------------------------------
def text_to_speech(text, language='en'):
    try:
        if not text:
            return None

        print(f"Generating speech for: '{text}' in {language}")

        filename = f"audio_{uuid.uuid4()}.mp3"
        filepath = os.path.join('media', 'audio', filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        tts = gTTS(text=text, lang=language)
        tts.save(filepath)

        print(f"Audio saved to: {filepath}")
        return f"audio/{filename}"

    except Exception as e:
        print(f"Error generating speech: {e}")
        return None
