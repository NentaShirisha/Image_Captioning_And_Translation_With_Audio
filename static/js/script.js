function uploadImage() {
    const form = document.getElementById('uploadForm');
    if (!form) return; // Not on upload page

    const formData = new FormData(form);
    const btn = document.getElementById('generateBtn');
    const spinner = btn ? btn.querySelector('.spinner-border') : null;
    const resultSection = document.querySelector('.result-section');

    // Show loading
    if (btn) btn.disabled = true;
    if (spinner) spinner.classList.remove('d-none');
    if (resultSection) resultSection.classList.add('d-none');

    fetch('/generate/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (response.status === 401) {
            // Not authenticated, redirect to login
            window.location.href = '/accounts/login/?next=/';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.error) {
            alert(data.error);
        } else if (data) {
            const captionEl = document.getElementById('caption');
            const translationEl = document.getElementById('translation');
            const audioEl = document.getElementById('audioPlayer');
            const imageEl = document.getElementById('resultImage');
            
            if (captionEl) captionEl.textContent = data.caption;
            if (translationEl) translationEl.textContent = data.translation;
            if (audioEl) audioEl.src = data.audio_url;
            if (imageEl) imageEl.src = data.image_url;
            if (resultSection) resultSection.classList.remove('d-none');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    })
    .finally(() => {
        if (btn) btn.disabled = false;
        if (spinner) spinner.classList.add('d-none');
    });
}