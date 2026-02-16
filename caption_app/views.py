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
            # Save image
            image_path = default_storage.save(f'uploads/{image.name}', image)
            full_path = os.path.join('media', image_path)
            
            try:
                # Process synchronously for now (can be made async with Celery)
                caption = generate_caption(full_path)
                translated = translate_text(caption, language)
                audio_path = text_to_speech(translated, language)
                
                # Save to DB only if user is authenticated
                if request.user.is_authenticated:
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
                return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'})

class CaptionAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        image = request.FILES.get('image')
        language = request.data.get('language', 'en')
        
        if image:
            image_path = default_storage.save(f'uploads/{image.name}', image)
            full_path = os.path.join('media', image_path)
            
            caption = generate_caption(full_path)
            translated = translate_text(caption, language)
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
        
        return Response({'error': 'No image provided'}, status=400)