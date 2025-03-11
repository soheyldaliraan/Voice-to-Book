# تبدیل صدا به متن کتاب فارسی 🎙️📚

<p align="center">
  <img src="/static/images/banner.png" alt="Voice to Book Banner" width="600">
  <br>
  <em>تبدیل صدای فارسی به متن ویرایش شده با قابلیت ذخیره سازی</em>
</p>

<div align="center">
  <h3>✨ <a href="https://voice-to-book.soheyl-daliraan.com/" target="_blank">Try the Live Demo</a> ✨</h3>
  <p><b>🌐 https://voice-to-book.soheyl-daliraan.com/ 🌐</b></p>
</div>

<div align="center">
  <b><a href="#-persian-voice-to-text-converter">⬇️ English information available below ⬇️</a></b>
</div>

<br>

<div dir="rtl">

## 🔍 این برنامه چیست؟ 
یک ابزار بسیار ساده برای تبدیل یادداشت های روزمره به مقاله ویرایش شده آماده ثبت در کتاب

## 💡 چرا این ابزار ایجاد شد؟
پدر من تعداد خیلی زیادی دست نوشته از زمان جوانی با خود به همراه دارد که به دلیل اینکه خیلی از آنها با خط شکسته نوشته شده اند، توسط مدل های تصویر به متن قابل شناسایی نیستند. سریع ترین راهی که می توان این نوشته ها را به فایل متنی تبدیل کرد، این است که کسی این ها را بخواند و بر اساس متن آنها نوشتار ایحاد شود
با اینکار می توان مطمین شد که نوشته ها و تجربیات ارزشمند پدرم برای نسل اینده حفظ می شود

## 👥 این ابزار برای چه کسانی ایجاد شده است ؟
برای کسانی مثل پدر من که کار کردن با چت جی پی تی یا ابزار های مشابه برای آنها بسیار سخت است ولی علاقه مند هستند تا تاثیر هوش مصنوعی را در زندگی خود ببینند


## 📝 راهنمای استفاده
این برنامه به شما امکان می‌دهد صدای فارسی را به متن تبدیل کنید. برای استفاده:

1. **🎤 ضبط صدا**: روی دکمه "شروع ضبط" کلیک کنید و صحبت کنید
2. **⏹️ توقف ضبط**: پس از اتمام صحبت، روی دکمه "توقف" کلیک کنید
3. **☁️ آپلود**: صدای ضبط شده را بررسی کرده و روی "آپلود صدا" کلیک کنید
4. **⚙️ پردازش**: پس از آپلود، روی دکمه "پردازش" کلیک کنید
5. **📋 دریافت متن**: متن پردازش شده را می‌توانید کپی یا دانلود کنید

### ✨ ویژگی‌ها
- تبدیل صدای فارسی به متن با دقت بالا
- ویرایش خودکار متن و اضافه کردن علائم نگارشی
- امکان دانلود متن پردازش شده
- نگهداری تاریخچه فایل‌های صوتی
- رابط کاربری ساده و کاربرپسند

### 🔧 نیازمندی‌ها
- مرورگر مدرن با پشتیبانی از ضبط صدا
- اتصال اینترنت پایدار
- میکروفون

</div>

---

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#️-tech-stack">Tech Stack</a> •
  <a href="#-prerequisites">Prerequisites</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#️-api-configuration">API Configuration</a> •
  <a href="#-development">Development</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a> •
  <a href="#-support">Support</a>
</p>

# 🎤 Persian Voice to Text Converter

A web application that converts Persian (Farsi) speech to text using Google Cloud Speech-to-Text API and enhances the output using OpenAI's GPT model.

## ✨ Features

- 🎤 Real-time audio recording
- 🈯 Persian speech-to-text conversion
- ✍️ Automatic text formatting and punctuation
- 📂 File history management
- 💾 Downloadable text output
- 📱 Mobile-responsive design

## 🛠️ Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: 
  - Google Cloud Speech-to-Text
  - OpenAI GPT
- **Storage**: Google Cloud Storage
- **Containerization**: Docker

## 📋 Prerequisites

- Python 3.12+
- Google Cloud Platform account
- OpenAI API key
- Docker (optional)

## 🚀 Installation

### 🐳 Using Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/voice_to_book.git
cd voice_to_book
```

2. Create environment files:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

### 💻 Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/voice_to_book.git
cd voice_to_book
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=path/to/gcloud-key.json
export GCS_BUCKET_NAME=your-bucket-name
export OPENAI_API_KEY=your-openai-api-key
```

5. Run the application:
```bash
python app.py
```

## 📱 Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Click "Start Recording" to begin recording your Persian speech
3. Click "Stop" when you're finished speaking
4. Review the recording and click "Upload Audio"
5. After uploading, click "Process" to convert speech to text
6. View, copy, or download the processed text

## 📂 Project Structure

```
├── app.py                 # Main Flask application
├── services/
│   ├── audio_service.py   # Audio processing service
│   └── text_service.py    # Text formatting service
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       └── main.js        # Frontend JavaScript
├── templates/
│   └── index.html         # Main HTML template
├── utils/
│   └── gcs_utils.py       # Google Cloud Storage utilities
├── assets/                # Audio file storage
├── outputs/               # Processed text outputs
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── .env.example           # Example environment variables
```

## ⚙️ API Configuration

### 🔑 Google Cloud Platform Setup

1. Create a new project in Google Cloud Console
2. Enable Speech-to-Text API
3. Create a service account with appropriate permissions
4. Download the service account key as JSON
5. Place the JSON file in your project and set the path in environment variables

### 🤖 OpenAI Setup

1. Create an account at [OpenAI](https://platform.openai.com/)
2. Generate an API key from the dashboard
3. Add the key to your environment variables

## 👨‍💻 Development

### 🧪 Running Tests
```bash
python -m pytest tests/
```

### 🧹 Code Style
The project follows PEP 8 guidelines. Run linting with:
```bash
flake8 .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the maintainer.

## 👤 Author

Soheyl Daliraan - [Website](https://soheyl-daliraan.com)

## 🙏 Acknowledgments

- Google Cloud Speech-to-Text API for speech recognition
- OpenAI GPT for text enhancement
- Flask framework and its community

---

<p align="center">
  Made with ❤️ by Soheyl Daliraan
</p>
