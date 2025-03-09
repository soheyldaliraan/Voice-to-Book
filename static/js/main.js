// Convert English numbers to Persian
function toPersianNum(num) {
    const persianNumbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return num.toString().replace(/[0-9]/g, function(w) {
        return persianNumbers[+w];
    });
}

// Audio Recording functionality
let mediaRecorder;
let recordedChunks = [];
let startTime;
let timerInterval;

const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const audioPreview = document.getElementById('audioPreview');
const timerDisplay = document.querySelector('.timer');
const recordingControls = document.getElementById('recordingControls');
const recordAgainButton = document.getElementById('recordAgain');
const recordingForm = document.getElementById('recordingForm');

function resetRecording() {
    audioPreview.style.display = 'none';
    recordingControls.style.display = 'none';
    recordButton.style.display = 'inline-block';
    stopButton.style.display = 'none';
    timerDisplay.textContent = '۰۰:۰۰';
    recordedChunks = [];
}

function updateTimer() {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
    const seconds = (elapsed % 60).toString().padStart(2, '0');
    timerDisplay.textContent = `${toPersianNum(minutes)}:${toPersianNum(seconds)}`;
}

recordButton.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        recordedChunks = [];
        
        mediaRecorder.addEventListener('dataavailable', (e) => {
            if (e.data.size > 0) recordedChunks.push(e.data);
        });
        
        mediaRecorder.addEventListener('stop', () => {
            const audioBlob = new Blob(recordedChunks, { type: 'audio/webm' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPreview.src = audioUrl;
            audioPreview.style.display = 'block';
            
            // Create a File object from the Blob
            const file = new File([audioBlob], 'recording.webm', { type: 'audio/webm' });
            
            // Create a FileList-like object
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            
            // Set the file input's files
            document.getElementById('audioBlob').files = dataTransfer.files;
            recordingControls.style.display = 'block';
        });
        
        mediaRecorder.start();
        startTime = Date.now();
        timerInterval = setInterval(updateTimer, 1000);
        
        recordButton.style.display = 'none';
        stopButton.style.display = 'inline-block';
        recordButton.classList.add('recording');
        
    } catch (err) {
        console.error('Error accessing microphone:', err);
        alert('خطا در دسترسی به میکروفون. لطفا مجوز دسترسی به میکروفون را تایید کنید.');
    }
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    clearInterval(timerInterval);
    recordButton.style.display = 'none';
    stopButton.style.display = 'none';
    recordButton.classList.remove('recording');
    
    // Stop all audio tracks
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
});

recordAgainButton.addEventListener('click', () => {
    resetRecording();
});

function copyText() {
    const textarea = document.getElementById('processedText');
    textarea.select();
    document.execCommand('copy');
    alert('متن کپی شد!');
}

function toggleLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

// Show loading when clicking process buttons
document.querySelectorAll('.file-item .button').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        toggleLoading(true);
        window.location.href = button.href;
    });
});

// Show loading when submitting the recording form
document.getElementById('recordingForm').addEventListener('submit', () => {
    toggleLoading(true);
});

// Hide loading if there was an error (check for flash messages)
document.addEventListener('DOMContentLoaded', () => {
    const errorMessages = document.querySelectorAll('.flash-error');
    if (errorMessages.length > 0) {
        toggleLoading(false);
    }
});
