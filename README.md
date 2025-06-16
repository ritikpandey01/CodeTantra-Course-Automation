Course Automation Script
This Python script automates online courses on any e-learning platform. Using Playwright for browser navigation and Groq for quiz answers, it’s built to handle multiple-choice, text, and coding questions. Customize it easily to fit your platform and course, saving you time and effort.

Features

Flexible: Works with any platform by editing config.json.
Quiz Support: Solves multiple-choice, text, and coding questions.
Automated Flow: Handles login, course selection, and quiz navigation.
Secure: Stores credentials in .env, ignored by Git.
Debug-Friendly: Logs details in quiz_automation.log and shows browser actions.


Setup Guide
Follow these steps to get the script running:
1. Clone the Repository
git clone https://github.com/your-username/CourseBlaze.git
cd CourseBlaze

2. Install Dependencies
Install required packages and Playwright browsers:
pip install -r requirements.txt
playwright install

3. Set Up Credentials

Copy the template:cp env.example .env


Edit .env with your platform login and Groq API key:PLATFORM_EMAIL=your_email@example.com
PLATFORM_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key

Note: .env is excluded from Git for security.

4. Configure Your Platform

Copy the config template:cp config.example.json config.json


Edit config.json for your platform:
Platform Details: Set url, course_name, and course_frame (if iframes are used).
Navigation: Define login, course_navigation, contents_navigation, and back_to_contents using Playwright selectors. Find role and name in browser dev tools (F12).
Course Structure: Add units and subtopics with quiz names from the platform.
Quiz Prompts: Set quiz_prompt for multiple-choice/text and code_prompt for coding questions.
Example:{
  "platform": "LearningPlatform",
  "url": "https://platform.com/login",
  "course_name": "Python Basics",
  "course_frame": "",
  "login": {
    "email": {"role": "textbox", "name": "Email"},
    "password": {"role": "textbox", "name": "Password"},
    "button": {"role": "button", "name": "Login"}
  },
  "units": [
    {
      "name": "Module 1",
      "subtopics": [
        {"name": "Introduction", "quiz": "Quiz 1"}
      ]
    }
  ]
}





5. Customize the Script (Optional)
The script supports multiple-choice, text, and coding questions. For other types (e.g., drag-and-drop):

Edit automate_platform.py, update solve_quiz to detect new question types.
Add functions like handle_drag_drop_question, similar to handle_code_question.
Add new prompts to config.json if needed.
Adjust timeouts in the script for slow platforms.

6. Run the Script
python automate_platform.py


The browser opens (headless=False) for debugging.
Check quiz_automation.log for progress and errors.


Customization Tips
Tailor the script to your platform:

Platform UI: Use browser dev tools to find selectors (e.g., role="button", name="Submit") and add them to config.json.
Course Layout: Match units and subtopics in config.json to your course’s structure.
Question Types:
Multiple-Choice/Text: Tune quiz_prompt for your platform’s quiz format.
Coding: Adjust code_prompt for languages like Python or Java.
Others: Add logic to solve_quiz in automate_platform.py for drag-and-drop or file uploads, with new prompts in config.json.


Debugging:
Use headless=False to watch the script.
Check quiz_automation.log for errors like “button not found” and fix selectors or timeouts.
Test one quiz to validate config.json.




Notes

Accuracy: Groq’s answers depend on prompts and page content. Test quiz_prompt and code_prompt for best results.
Platform Issues: CAPTCHAs or complex logins may need manual steps or script changes.
Question Types: Supports multiple-choice, text, and coding. Others need code updates.
Usage: Respect your platform’s rules and use ethically.


Contact
Questions or suggestions? Open an issue on GitHub. Happy automating! 😎
