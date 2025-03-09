from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import logging
from services.audio_service import AudioService
from services.text_service import TextService

# Load environment variables
load_dotenv(override=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'assets'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'.wav', '.webm', '.ogg', '.flac'}  # Formats supported by Google Speech-to-Text

# Create necessary directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path('outputs').mkdir(exist_ok=True)

# Initialize services
audio_service = AudioService(app.config['UPLOAD_FOLDER'], ALLOWED_EXTENSIONS)
text_service = TextService()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 3
    audio_files = audio_service.get_audio_files()
    
    # Calculate pagination
    total_files = len(audio_files)
    total_pages = (total_files + per_page - 1) // per_page  # Ceiling division
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_files = audio_files[start_idx:end_idx]
    
    return render_template('index.html', 
                         audio_files=paginated_files,
                         current_page=page,
                         total_pages=total_pages,
                         processed_text=None,
                         processed_file=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files and 'audio_blob' not in request.files:
        flash('فایلی انتخاب نشده است')
        return redirect(url_for('index'))
    
    file = request.files.get('file') or request.files.get('audio_blob')
    if file.filename == '':
        flash('فایلی انتخاب نشده است')
        return redirect(url_for('index'))
    
    # Handle recorded audio (webm format)
    if file.filename == 'recording.webm' or file.content_type == 'audio/webm':
        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
    else:
        filename = secure_filename(file.filename)
    
    if file and (audio_service.allowed_file(filename) or filename.endswith('.webm')):
        filepath = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(filepath)
        flash('فایل با موفقیت آپلود شد')
        
        # Get paginated files like in index route
        page = 1  # Show first page after upload
        per_page = 3
        audio_files = audio_service.get_audio_files()
        
        # Calculate pagination
        total_files = len(audio_files)
        total_pages = (total_files + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_files = audio_files[start_idx:end_idx]
        
        return render_template('index.html', 
                             audio_files=paginated_files,
                             current_page=page,
                             total_pages=total_pages,
                             processed_text=None,
                             processed_file=None)
    
    flash('نوع فایل نامعتبر است')
    return redirect(url_for('index'))

@app.route('/process/<filename>')
def process_file(filename):
    try:
        filepath = Path(app.config['UPLOAD_FOLDER']) / filename
        if not filepath.exists():
            flash('فایل پیدا نشد')
            return redirect(url_for('index'))
        
        # Process the file
        transcribed_text = audio_service.transcribe_audio(filepath)
        formatted_article = text_service.format_as_article(transcribed_text)
        
        # Save the result
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"{Path(filename).stem}_{timestamp}_article.txt"
        output_path = Path('outputs') / output_filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted_article)
        
        # Get paginated files
        page = 1  # Show first page after processing
        per_page = 3
        audio_files = audio_service.get_audio_files()
        
        # Calculate pagination
        total_files = len(audio_files)
        total_pages = (total_files + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_files = audio_files[start_idx:end_idx]
        
        flash('پردازش با موفقیت انجام شد')
        return render_template('index.html', 
                             audio_files=paginated_files,
                             current_page=page,
                             total_pages=total_pages,
                             processed_text=formatted_article,
                             processed_file=filename)
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        flash('خطایی در پردازش رخ داد')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('outputs', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 