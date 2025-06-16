🎯 Course Automation Script
Welcome to the Course Automation Script—a smart tool to automate your online courses on any e-learning platform! Powered by Playwright for smooth browser navigation and Groq for answering quizzes, this script is super flexible. Whether it’s multiple-choice, text-based, or coding questions, you can tweak it to fit any platform or course. Ready to save time? Let’s go! 🚀

🌟 What’s Cool About It?

Works Anywhere: Customize config.json for any learning platform.
Handles All Quizzes: Solves multiple-choice, text, and coding questions with Groq’s help.
Easy Navigation: Automates login, course selection, and quiz access.
Secure Setup: Keeps your email and password safe in .env.
Debug Made Simple: Logs everything in quiz_automation.log and shows the browser in action.


🛠️ How to Set It Up
Get the script running in no time with these steps:
1. Clone the Repository
git clone https://github.com/your-username/course-automation.git
cd course-automation

2. Install Dependencies
Grab the required Python packages and Playwright browsers:
pip install playwright groq python-dotenv
playwright install

3. Add Your Details
Keep your credentials safe:

Copy the template:cp env.example .env


Edit .env with your platform login and Groq API key:PLATFORM_EMAIL=your_email@example.com
PLATFORM_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key

Note: .env stays private, thanks to .gitignore.

4. Set Up Your Platform
Make the script work for your platform:

Copy the config template:cp config.example.json config.json


Edit config.json to match your platform and course:
Platform Info: Add url, course_name, and course_frame (if the platform uses iframes).
Navigation: Set login, course_navigation, contents_navigation, and back_to_contents using Playwright selectors. Use browser developer tools (F12) to find role and name attributes.
Course Layout: List units and subtopics with quiz names as they appear on the platform.
Quiz Answers: Adjust quiz_prompt for multiple-choice or text questions and code_prompt for coding tasks.
Example:{
  "platform": "YourPlatform",
  "url": "https://yourplatform.com/login",
  "course_name": "Learn Python",
  "course_frame": "",
  "login": {
    "email": {"role": "textbox", "name": "Email"},
    "password": {"role": "textbox", "name": "Password"},
    "button": {"role": "button", "name": "Sign In"}
  },
  "units": [
    {
      "name": "Module 1",
      "subtopics": [
        {"name": "Basics", "quiz": "Quiz 1"}
      ]
    }
  ]
}





5. Tweak the Script (If Needed)
The script handles multiple-choice, text, and coding questions by default. For other question types (like drag-and-drop):

Open automate_platform.py and update the solve_quiz function to detect new question types.
Add new functions (e.g., handle_drag_drop_question) like handle_code_question.
Update config.json with new prompts if required.
If your platform loads slowly, increase timeouts in the script or config.json.

6. Run the Script
Watch the automation in action:
python automate_platform.py


The browser opens (headless=False) so you can see what’s happening.
Check quiz_automation.log for progress and any issues.


🔧 How to Make It Yours
Customize the script to fit any platform or course:

Platform Setup: Use browser developer tools to find HTML selectors (e.g., role="button", name="Submit") and add them to config.json for login, navigation, and quiz buttons.
Course Structure: Map your course’s modules and quizzes in config.json’s units and subtopics. Use exact names from the platform.
Question Types:
Multiple-Choice/Text: Fine-tune quiz_prompt to match your platform’s quiz style.
Coding: Set code_prompt for languages like Python, Java, or others.
Other Types: For drag-and-drop or file uploads, add new logic to solve_quiz in automate_platform.py and new prompts in config.json.


Debugging Tips:
Run with headless=False to watch the script work.
Check quiz_automation.log for errors like “button not found” and fix selectors or timeouts.
Test with one quiz first to ensure config.json is correct.




⚠️ Things to Know

Answer Quality: Groq’s answers depend on good prompts and clear page content. Test quiz_prompt and code_prompt to get the best results.
Platform Challenges: CAPTCHAs or login redirects might need manual steps or extra code.
Question Types: The script covers multiple-choice, text, and coding. Other types need script updates.
Use Wisely: Follow your platform’s rules and use this to learn smarter!


👨‍💻 Who Made This?
Crafted with 💻 and a lot of chai! Questions or ideas? Drop an issue on GitHub. Now go ace those courses! 😎
