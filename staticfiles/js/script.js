function uploadImage() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);
    const btn = document.getElementById('generateBtn');
    const spinner = btn.querySelector('.spinner-border');
    const resultSection = document.querySelector('.result-section');

    // Show loading
    btn.disabled = true;
    spinner.classList.remove('d-none');
    resultSection.classList.add('d-none');

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
            document.getElementById('caption').textContent = data.caption;
            document.getElementById('translation').textContent = data.translation;
            document.getElementById('audioPlayer').src = data.audio_url;
            document.getElementById('resultImage').src = data.image_url;
            resultSection.classList.remove('d-none');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    })
    .finally(() => {
        btn.disabled = false;
        spinner.classList.add('d-none');
    });
}