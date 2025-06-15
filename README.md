# 🤖 CodeTantra Quiz Automation Tool

An intelligent automation tool that uses AI to solve CodeTantra platform quizzes automatically. The tool handles both multiple-choice questions and SQL queries using advanced language models.

## ✨ Features

- **🔐 Automated Login**: Seamless authentication with CodeTantra platform
- **🎯 Smart Navigation**: Automatically navigates through courses, units, and subtopics
- **🧠 AI-Powered Solutions**: 
  - Multiple choice questions solved using Groq AI
  - SQL queries generated and executed automatically
- **📊 Progress Tracking**: Detailed logging of automation progress
- **🔄 Error Recovery**: Robust error handling and retry mechanisms
- **⚡ Batch Processing**: Process multiple units and subtopics in sequence

## 🛠️ Technologies Used

- **Python 3.8+**
- **Playwright** - Web automation framework
- **Groq AI** - Language model for generating answers
- **Environment Variables** - Secure credential management

## 📋 Prerequisites

Before running this tool, make sure you have:

- Python 3.8 or higher installed
- A CodeTantra account with valid credentials
- Groq API key (free tier available)
- Chrome/Chromium browser installed

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/codetantra-quiz-automation.git
   cd codetantra-quiz-automation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   CODETANTRA_EMAIL=your_email@example.com
   CODETANTRA_PASSWORD=your_password
   GROQ_API_KEY=your_groq_api_key
   PLATFORM_URL=https://codetantra.com/login
   ```

5. **Configure course data**
   
   Update `data.json` with your course structure (see Configuration section)

## ⚙️ Configuration

### Course Configuration (`data.json`)

Structure your course data in the following format:

```json
{
  "course_name": "Your Course Name",
  "units": [
    {
      "name": "Unit 1 - Introduction",
      "subtopics": [
        {"name": "Topic Name", "quiz": "Quiz Title"},
        {"name": "Another Topic", "quiz": "Another Quiz"}
      ]
    }
  ]
}
```

### Environment Variables (`.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `CODETANTRA_EMAIL` | Your CodeTantra login email | ✅ |
| `CODETANTRA_PASSWORD` | Your CodeTantra password | ✅ |
| `GROQ_API_KEY` | Your Groq API key | ✅ |
| `PLATFORM_URL` | CodeTantra login URL | ✅ |

## 🎮 Usage

1. **Run the automation tool**
   ```bash
   python file.py
   ```

2. **Monitor progress**
   - Watch the browser automation in real-time
   - Check `quiz_automation.log` for detailed logs
   - View console output for progress updates

3. **Results**
   - The tool will automatically solve quizzes in sequence
   - Progress is logged for each question and subtopic
   - Browser remains open for debugging after completion

## 📁 Project Structure

```
quiz-automation/
├── file.py                 # Main automation script
├── data.json              # Course configuration
├── .env                   # Environment variables (not in repo)
├── requirements.txt       # Python dependencies
├── quiz_automation.log    # Generated log file
└── README.md             # This file
```

## 🔧 How It Works

1. **Authentication**: Logs into CodeTantra using provided credentials
2. **Navigation**: Automatically navigates to specified course and units
3. **Question Detection**: Identifies question types (MCQ vs SQL)
4. **AI Processing**: 
   - Sends question content to Groq AI
   - Receives intelligent answers/solutions
5. **Answer Submission**: Automatically selects answers and submits
6. **Progress Tracking**: Moves through all configured subtopics

## 📊 Logging

The tool provides comprehensive logging:

- **Console Output**: Real-time progress updates
- **Log File**: Detailed execution logs in `quiz_automation.log`
- **Error Tracking**: Detailed error messages and retry attempts

⚠️ **Educational & Research Purpose Only**
This tool is developed for:
- Learning web automation techniques
- Understanding AI integration
- Educational research purposes
- Demonstrating Playwright capabilities

**Not intended for academic dishonesty or violating platform ToS**


## 🔮 Future Enhancements

- [ ] Support for more question types
- [ ] GUI interface for easier configuration
- [ ] Multiple platform support
- [ ] Enhanced AI model integration
- [ ] Batch course processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## ⚡ Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/codetantra-quiz-automation.git
cd codetantra-quiz-automation
pip install -r requirements.txt
playwright install chromium

# Configure
cp .env.example .env
# Edit .env with your credentials

# Run
python file.py
```

