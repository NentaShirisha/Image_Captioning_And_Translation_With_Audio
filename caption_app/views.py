from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CaptionHistory
from .serializers import CaptionHistorySerializer
from .ai_engine import generate_caption, translate_text, text_to_speech
import os

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def upload(request):
    return render(request, 'upload.html')

@login_required
def history(request):
    history = CaptionHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'history': history})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@csrf_exempt
def generate_caption_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    if request.method == 'POST':
        image = request.FILES.get('image')
        language = request.POST.get('language', 'en')

        if image:
            try:
                # Save uploaded image
                image_path = default_storage.save(f'uploads/{image.name}', image)
                full_path = os.path.join('media', image_path)

                # 🔴 CPU-safe caption generation
                caption = generate_caption(full_path)

                if not caption:
                    raise Exception("Caption generation failed")

                # Translation fallback safety
                translated = translate_text(caption, language)
                if not translated:
                    translated = caption

                # Audio generation
                audio_path = text_to_speech(translated, language)

                # Save history
                history = CaptionHistory.objects.create(
                    user=request.user,
                    image=image_path,
                    caption=caption,
                    language=language,
                    translated_text=translated,
                    audio_file=audio_path
                )

                return JsonResponse({
                    'caption': caption,
                    'translation': translated,
                    'audio_url': f'/media/{audio_path}',
                    'image_url': f'/media/{image_path}'
                })

            except Exception as e:
                print("Caption Error:", str(e))
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

class CaptionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image = request.FILES.get('image')
        language = request.data.get('language', 'en')

        if image:
            try:
                image_path = default_storage.save(f'uploads/{image.name}', image)
                full_path = os.path.join('media', image_path)

                caption = generate_caption(full_path)
                if not caption:
                    raise Exception("Caption generation failed")

                translated = translate_text(caption, language)
                if not translated:
                    translated = caption

                audio_path = text_to_speech(translated, language)

                history = CaptionHistory.objects.create(
                    user=request.user,
                    image=image_path,
                    caption=caption,
                    language=language,
                    translated_text=translated,
                    audio_file=audio_path
                )

                serializer = CaptionHistorySerializer(history)
                return Response(serializer.data)

            except Exception as e:
                print("API Caption Error:", str(e))
                return Response({'error': str(e)}, status=500)

        return Response({'error': 'No image provided'}, status=400)
