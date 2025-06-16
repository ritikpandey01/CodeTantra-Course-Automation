# 🚀 Course Automation Script

A powerful Python script that automates online courses on **any e-learning platform**. Using Playwright for seamless browser navigation and Groq AI for intelligent quiz solving, this tool handles multiple-choice, text-based, and coding questions with ease.

## ✨ Key Features

- **🌐 Universal Compatibility**: Easily adapt to any e-learning platform through simple configuration
- **🧠 AI-Powered Quiz Solver**: Tackles multiple-choice, text, and coding questions using Groq API
- **🤖 Automated Navigation**: Handles login, course access, and quiz navigation automatically
- **🔐 Secure Credential Management**: Stores sensitive information in `.env` files (Git-ignored)
- **📊 Comprehensive Logging**: Detailed logs in `quiz_automation.log` for easy debugging
- **👀 Visual Debugging**: Browser visibility option for troubleshooting

## 📋 Prerequisites

- Python 3.8 or higher
- A Groq API key ([Get one here](https://console.groq.com/))
- Access to an online course platform

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/course-automation.git
cd course-automation
```

### 2. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 3. Set Up Environment Variables

```bash
# Copy the environment template
cp env.example .env
```

Edit the `.env` file with your credentials:

```env
PLATFORM_EMAIL=your_email@example.com
PLATFORM_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key
```

> **Note**: The `.env` file is automatically ignored by Git for security.

### 4. Configure Your Platform

```bash
# Copy the configuration template
cp config.example.json config.json
```

Edit `config.json` to match your platform. Here's what you need to configure:

#### Platform Settings
- **url**: Login page URL
- **course_name**: Name of your course
- **course_frame**: iframe selector (if applicable)

#### Navigation Selectors
Use browser dev tools (F12) to find Playwright selectors:
- **login**: Email, password, and button selectors
- **course_navigation**: Course access elements
- **contents_navigation**: Content navigation elements
- **back_to_contents**: Return navigation elements

#### Course Structure
- **units**: Array of course modules
- **subtopics**: Topics within each unit
- **quiz**: Quiz names for each subtopic

#### AI Prompts
- **quiz_prompt**: Instructions for multiple-choice/text questions
- **code_prompt**: Instructions for coding questions

#### Example Configuration

```json
{
  "platform": "LearningPlatform",
  "url": "https://platform.com/login",
  "course_name": "Python Fundamentals",
  "course_frame": "",
  "login": {
    "email": {"role": "textbox", "name": "Email"},
    "password": {"role": "textbox", "name": "Password"},
    "button": {"role": "button", "name": "Sign In"}
  },
  "course_navigation": {
    "role": "link",
    "name": "Start Course"
  },
  "units": [
    {
      "name": "Module 1: Python Basics",
      "subtopics": [
        {
          "name": "Introduction to Python",
          "quiz": "Python Basics Quiz"
        },
        {
          "name": "Variables and Data Types",
          "quiz": "Variables Quiz"
        }
      ]
    }
  ],
  "quiz_prompt": "Answer this quiz question based on the context provided...",
  "code_prompt": "Write Python code to solve this programming problem..."
}
```

## 🚀 Usage

Run the automation script:

```bash
python automate_platform.py
```

The script will:
1. Open a browser window (visible for debugging)
2. Log into your platform
3. Navigate to your course
4. Complete quizzes automatically
5. Log all activities to `quiz_automation.log`

## 🔧 Customization

### Adding New Question Types

The script currently supports multiple-choice, text, and coding questions. To add support for other types (e.g., drag-and-drop):

1. **Modify the main script**:
   ```python
   # In automate_platform.py, update the solve_quiz function
   def solve_quiz(page, config):
       # Add detection for new question types
       if page.locator("drag-drop-container").is_visible():
           handle_drag_drop_question(page, config)
   ```

2. **Add new handler functions**:
   ```python
   def handle_drag_drop_question(page, config):
       # Your drag-and-drop logic here
       pass
   ```

3. **Update configuration**:
   ```json
   {
     "drag_drop_prompt": "Instructions for drag-and-drop questions..."
   }
   ```

### Platform-Specific Adjustments

- **Slow platforms**: Increase timeout values in the script
- **Complex navigation**: Add additional selectors to `config.json`
- **Special authentication**: Modify login logic in `automate_platform.py`

## 📝 Debugging Tips

### Common Issues and Solutions

1. **"Element not found" errors**:
   - Use browser dev tools to verify selectors
   - Check if elements are in iframes
   - Increase wait times for slow-loading content

2. **Login failures**:
   - Verify credentials in `.env` file
   - Check for CAPTCHAs (may require manual intervention)
   - Ensure selectors match the actual login form

3. **Quiz not being solved**:
   - Review `quiz_automation.log` for detailed error messages
   - Test prompts with individual questions
   - Verify Groq API key is valid

### Debugging Mode

The script runs with `headless=False` by default, allowing you to:
- Watch the automation in real-time
- Identify where the script gets stuck
- Manually intervene if needed

## 📊 Logging

All activities are logged to `quiz_automation.log`:
- Login attempts and success/failure
- Course navigation steps
- Quiz questions and AI responses
- Error messages and stack traces

## ⚠️ Important Considerations

### Answer Quality
- AI responses depend on prompt quality and page content
- Fine-tune `quiz_prompt` and `code_prompt` for better accuracy
- Consider the context provided to the AI model

### Platform Limitations
- Some platforms may have CAPTCHAs or anti-bot measures
- Complex authentication flows may require manual intervention
- Rate limiting might affect performance

### Supported Question Types
- ✅ Multiple-choice questions
- ✅ Text-based questions
- ✅ Coding questions
- ❌ Drag-and-drop (requires customization)
- ❌ File upload questions (requires customization)

### Ethical Usage
- Use responsibly and in accordance with your platform's terms of service
- Respect rate limits and platform policies
- Consider the educational value of automated completion

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Areas for Improvement
- Support for additional question types
- GUI interface for easier configuration
- Multi-platform configuration templates
- Enhanced error handling and recovery

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

Having trouble? Here's how to get help:

1. **Check the logs**: Review `quiz_automation.log` for detailed error information
2. **Browse existing issues**: Look through [GitHub Issues](https://github.com/your-username/course-automation/issues)
3. **Create a new issue**: Provide detailed information about your problem
4. **Join discussions**: Participate in [GitHub Discussions](https://github.com/your-username/course-automation/discussions)

## 🎯 Roadmap

- [ ] GUI configuration interface
- [ ] Support for more question types
- [ ] Multi-course automation
- [ ] Progress tracking and analytics
- [ ] Integration with popular learning platforms

---

**Happy Learning!** 🎓 Automate your courses responsibly and focus on understanding the concepts that matter most.

*Made with ❤️ by developers, for learners*
