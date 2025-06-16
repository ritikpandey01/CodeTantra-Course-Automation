# 🎯 Course Automation Script

**Automate any online course with AI-powered quiz solving!** 

A smart Python script that handles course navigation and quiz completion on any e-learning platform using Playwright and Groq AI. Simply configure it once for your platform and let it do the work.

---

## ✨ Features

🌐 **Universal Platform Support** - Works with any e-learning platform  
🧠 **AI Quiz Solver** - Handles multiple-choice, text, and coding questions  
🤖 **Smart Navigation** - Automates login, course access, and quiz flow  
🔐 **Secure Setup** - Credentials stored safely in `.env` files  
📊 **Detailed Logging** - Track everything in `quiz_automation.log`  
🛠️ **Fully Customizable** - Adapt to any platform or course structure  

---

## 🚀 Quick Start

### 1️⃣ Clone & Install
```bash
git clone https://github.com/ritikpandey01/Course-Automation
cd course-automation
pip install -r requirements.txt
playwright install
```

### 2️⃣ Setup Credentials
Create a `.env` file:
```env
PLATFORM_EMAIL=your_email@example.com
PLATFORM_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key
```

### 3️⃣ Configure Your Platform
Edit `config.json` to match your platform and course:

```json
{
  "platform": "YourPlatform",
  "url": "https://yourplatform.com/login",
  "course_name": "Your Course Name",
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
  "contents_navigation": {
    "role": "button",
    "name": "Contents"
  },
  "back_to_contents": {
    "role": "link",
    "name": "Back to Course"
  },
  "units": [
    {
      "name": "Module 1",
      "subtopics": [
        {"name": "Introduction", "quiz": "Quiz 1"},
        {"name": "Basics", "quiz": "Quiz 2"}
      ]
    }
  ],
  "submit_buttons": [
    {"role": "button", "name": "Submit"},
    {"role": "button", "name": "Next"}
  ],
  "next_buttons": [
    {"role": "button", "name": "Next"},
    {"role": "button", "name": "Continue"}
  ],
  "quiz_prompt": "You are a helpful assistant. Answer this quiz question based on the provided context. Give only the answer, no explanations.",
  "code_prompt": "You are a coding assistant. Write clean, working code to solve this programming problem. Only provide the code solution."
}
```

### 4️⃣ Run the Script
```bash
python automate_platform.py
```

The browser will open and automate your course. Check `quiz_automation.log` for progress!

---

## ⚙️ Configuration Guide

### Finding Selectors
Use browser dev tools (F12) to find the right selectors:
1. Right-click on elements → Inspect
2. Look for `role` and `name` attributes
3. Use formats like: `{"role": "button", "name": "Submit"}`

### Platform Adaptation
**Every platform is different!** Modify these sections in `config.json`:

- **URLs**: Update login and course URLs
- **Selectors**: Find platform-specific button/input selectors  
- **Course Structure**: Map your actual units and subtopics
- **Navigation Flow**: Adjust navigation elements
- **Prompts**: Customize AI prompts for better answers

### Question Types Supported
- ✅ **Multiple Choice** - AI picks the best option
- ✅ **Text Questions** - AI provides written answers  
- ✅ **Coding Problems** - AI writes complete code solutions
- 🔧 **Others** - Extend the script for drag-drop, file uploads, etc.

---

## 🛠️ Customization

### Adding New Question Types
Want to handle drag-and-drop or other question types? 

1. **Detect the question type** in `solve_quiz()` function:
```python
if page.locator(".drag-drop-container").is_visible():
    handle_drag_drop_question(page, config)
```

2. **Create handler function**:
```python
def handle_drag_drop_question(page, config):
    # Your custom logic here
    pass
```

3. **Add prompts** to `config.json`:
```json
{
  "drag_drop_prompt": "Instructions for drag-and-drop questions..."
}
```

### Platform-Specific Tweaks
- **Slow loading?** Increase timeout values in the script
- **Complex navigation?** Add more selectors to config
- **Special auth?** Modify login logic in the main script
- **Different layout?** Adjust course structure mapping

---

## 🔍 Debugging

### Check the Logs
Everything is logged in `quiz_automation.log`:
- Login success/failure
- Navigation steps  
- Quiz questions and AI responses
- Error messages with details

### Common Issues
- **"Element not found"** → Check selectors in browser dev tools
- **Login fails** → Verify credentials and check for CAPTCHAs  
- **Wrong answers** → Improve AI prompts in config
- **Timeouts** → Increase wait times for slow platforms

### Debug Mode
Script runs with visible browser (`headless=False`) so you can:
- Watch the automation live
- See where it gets stuck
- Manually intervene if needed

---

## ⚠️ Important Notes

### AI Answer Quality
- Answers depend on your prompts and page content
- Fine-tune `quiz_prompt` and `code_prompt` for better results
- Test with a few questions first

### Platform Limitations  
- Some platforms have anti-bot measures
- CAPTCHAs may require manual solving
- Rate limiting might slow things down

### Responsible Usage
- Follow your platform's terms of service
- Use for learning, not cheating
- Understand the material, don't just complete it

---

## 🤝 Contributing

Want to improve the script? Here's how:

1. Fork the repo
2. Create a feature branch: `git checkout -b cool-feature`
3. Make your changes
4. Commit: `git commit -m 'Add cool feature'`
5. Push: `git push origin cool-feature`  
6. Open a Pull Request

**Ideas for contributions:**
- Support for more question types
- Better error handling
- Performance improvements
- Platform-specific templates

---

## 🎯 What's Next?

- [ ] GUI interface for easier setup
- [ ] More question type handlers
- [ ] Better AI prompt engineering
- [ ] Multi-course batch processing
- [ ] Progress analytics and reporting


---

**Ready to automate your courses?** 🚀 

Configure `config.json` for your platform, run the script, and watch the magic happen. Check the logs if anything goes wrong!
