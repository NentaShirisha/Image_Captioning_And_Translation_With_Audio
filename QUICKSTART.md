# AI Vision Platform - Quick Start Guide

## 🚀 Getting Started

1. **Navigate to project directory:**
   ```bash
   cd ai_vision_platform
   ```

2. **Create virtual environment (if not done):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database:**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow prompts to create username, email, password.

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main app: http://127.0.0.1:8000
   - Admin panel: http://127.0.0.1:8000/admin

## 🔧 Additional Setup (Optional)

### For Celery (Background Tasks):
1. Install Redis
2. Run Celery worker:
   ```bash
   celery -A ai_vision_platform worker -l info
   ```

### For Production:
- Switch to PostgreSQL in settings.py
- Configure static files serving
- Set up proper media storage

## 📱 API Usage

The platform provides REST API endpoints for integration:

```python
import requests

# Example API call
response = requests.post('http://127.0.0.1:8000/api/generate-caption/',
    files={'image': open('image.jpg', 'rb')},
    data={'language': 'hi'},
    headers={'Authorization': 'Token YOUR_TOKEN'}
)
```

## 🎯 Features Implemented

✅ Real-time image captioning with BLIP
✅ Multi-language translation
✅ Text-to-speech generation
✅ User authentication & dashboard
✅ History tracking
✅ REST API
✅ Admin analytics
✅ Modern Bootstrap UI
✅ Responsive design
✅ AJAX processing
✅ Database models
✅ Scalable architecture

## 🔮 Next Steps

- Deploy to cloud (AWS/Heroku)
- Add user registration emails
- Implement Celery for async processing
- Add more AI models
- Mobile app development
- Advanced analytics dashboard

Enjoy your AI Vision Platform! 🎉