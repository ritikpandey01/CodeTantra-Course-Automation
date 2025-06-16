from playwright.sync_api import Playwright, sync_playwright
from groq import Groq
import time
import re
from dotenv import load_dotenv
import os
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("quiz_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get credentials from environment variables
EMAIL = os.getenv("PLATFORM_EMAIL")
PASSWORD = os.getenv("PLATFORM_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

class QuizAutomation:
    def __init__(self, playwright, config_file):
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file):
        """Load JSON configuration file"""
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
                logger.info(f"Loaded configuration from {config_file}")
                return config
        except Exception as e:
            logger.error(f"Failed to load config file: {e}")
            raise
    
    def login(self):
        """Login to the platform"""
        try:
            logger.info(f"Logging in to {self.config['platform']}")
            self.page.goto(self.config['url'])
            self.page.get_by_role(self.config['login']['email']['role'], name=self.config['login']['email']['name']).fill(EMAIL)
            self.page.get_by_role(self.config['login']['password']['role'], name=self.config['login']['password']['name']).fill(PASSWORD)
            self.page.get_by_role(self.config['login']['button']['role'], name=self.config['login']['button']['name']).click()
            self.page.wait_for_timeout(2000)
            logger.info("Login successful")
            return True
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def navigate_to_course(self, course_name):
        """Navigate to the specified course"""
        try:
            logger.info(f"Navigating to course: {course_name}")
            self.page.get_by_role(self.config['course_navigation']['view_courses']['role'], name=self.config['course_navigation']['view_courses']['name']).click()
            self.page.wait_for_timeout(2000)
            
            first_frame = self.page.frame_locator(self.config['course_navigation']['frame']).first
            
            for attempt in range(3):
                try:
                    self.page.wait_for_timeout(5000)
                    button = first_frame.get_by_role("button", name=course_name)
                    if button.count() > 0:
                        button.click(timeout=60000)
                        logger.info(f"Clicked course button: {course_name}")
                        break
                    partial = self.config['course_navigation']['partial_match']
                    button = first_frame.get_by_role("button").filter(has_text=partial).first
                    if button.count() > 0:
                        button.click(timeout=60000)
                        logger.info(f"Clicked course button containing: {partial}")
                        break
                    link = first_frame.get_by_role("link").filter(has_text=partial).first
                    if link.count() > 0:
                        link.click(timeout=60000)
                        logger.info(f"Clicked course link containing: {partial}")
                        break
                    logger.warning(f"Attempt {attempt + 1}: Could not find course: {course_name}")
                    time.sleep(5)
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(5)
            else:
                logger.error("Failed to click course after 3 attempts.")
                return False
            
            self.page.wait_for_timeout(2000)
            return True
        except Exception as e:
            logger.error(f"Error navigating to course: {e}")
            return False
    
    def get_course_frame(self):
        """Get the course iframe"""
        course_frame = self.page.frame(self.config['course_frame'])
        if not course_frame:
            logger.error("Couldn't locate course iframe!")
            return None
        return course_frame
    
    def navigate_to_contents(self, course_frame):
        """Navigate to the Contents page"""
        try:
            course_frame.get_by_role(self.config['contents_navigation']['role'], name=self.config['contents_navigation']['name']).click()
            self.page.wait_for_timeout(2000)
            logger.info("Navigated to Contents page")
            return True
        except Exception as e:
            logger.error(f"Error navigating to Contents: {e}")
            return False
    
    def click_button_containing_text(self, course_frame, text, strict=False):
        """Click a button that contains the given text"""
        try:
            if strict:
                course_frame.get_by_role("button", name=text).first.click()
                return True
            
            buttons = course_frame.locator("button").all()
            for button in buttons:
                try:
                    button_text = button.inner_text()
                    if text.lower() in button_text.lower():
                        button.click()
                        logger.info(f"Clicked button with text: {button_text}")
                        return True
                except:
                    continue
                    
            buttons = course_frame.locator("div[role='button']").all()
            for button in buttons:
                try:
                    button_text = button.inner_text()
                    if text.lower() in button_text.lower():
                        button.click()
                        logger.info(f"Clicked div button with text: {button_text}")
                        return True
                except:
                    continue
            
            logger.warning(f"Could not find button containing text: {text}")
            return False
        except Exception as e:
            logger.error(f"Error clicking button containing text '{text}': {e}")
            return False
    
    def get_quiz_answer(self, page_content):
        """Get multiple choice or text answer from Groq"""
        try:
            prompt = self.config.get('quiz_prompt', """
Analyze this quiz page content. Find the question and options.
Then tell me ONLY the numbers of the correct options (e.g., "1, 3") for multiple-choice, or the exact answer text for text-based questions.
No explanation needed, no prefix, no suffix.
Page content:
{content}
""").format(content=page_content)
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            full_response = response.choices[0].message.content.strip()
            logger.info(f"Raw Groq response: {full_response}")
            
            if "correct options are:" in full_response.lower():
                answer_part = full_response.lower().split("correct options are:")[1].strip()
                indices = [int(num.strip()) for num in re.findall(r'\d+', answer_part)]
                answer_str = ", ".join(str(idx) for idx in indices)
            else:
                answer_str = full_response  # For text-based answers
                indices = [int(num.strip()) for num in re.findall(r'\d+', full_response) if num.strip().isdigit()]
                if indices:
                    answer_str = ", ".join(str(idx) for idx in indices)
            
            logger.info(f"Parsed answer: {answer_str}")
            return answer_str
        except Exception as e:
            logger.error(f"Groq error for quiz: {e}")
            return "1"
    
    def get_code_answer(self, page_content):
        """Get code answer from Groq"""
        try:
            prompt = self.config.get('code_prompt', """
You are a coding expert. Provide ONLY the code solution for the following problem, with no explanation or comments.
Problem:
{content}
Code:
""").format(content=page_content)
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            code = response.choices[0].message.content.strip()
            logger.info(f"Groq generated code: {code}")
            return code
        except Exception as e:
            logger.error(f"Groq error for code: {e}")
            return "# Default code"
    
    def has_submit_button(self, course_frame):
        """Check if the page has a submit/check/run button"""
        button_names = self.config.get('submit_buttons', ["Submit", "Check Answer", "Run", "Execute", "Verify"])
        
        for name in button_names:
            try:
                button = course_frame.get_by_role("button", name=name)
                if button.count() > 0:
                    return True
            except:
                pass
        
        buttons = course_frame.locator("button").all()
        for button in buttons:
            try:
                button_text = button.inner_text().lower()
                if any(name.lower() in button_text for name in button_names):
                    return True
            except:
                continue
        
        return False
    
    def has_checkboxes(self, course_frame):
        """Check if the page has checkboxes"""
        checkboxes = course_frame.locator("input[type='checkbox']").all()
        return len(checkboxes) > 0
    
    def has_code_editor(self, course_frame):
        """Check if the page has a code editor (textarea or specific class)"""
        try:
            # Look for textarea or common code editor classes (e.g., CodeMirror, ACE Editor)
            editors = course_frame.locator("textarea, .CodeMirror, .ace_editor, [contenteditable='true']").all()
            return len(editors) > 0
        except Exception as e:
            logger.error(f"Error checking for code editor: {e}")
            return False
    
    def handle_quiz_question(self, course_frame, page_content):
        """Handle multiple choice or text-based quiz questions"""
        try:
            answer = self.get_quiz_answer(page_content)
            logger.info(f"Groq says answer is: {answer}")
            
            if self.has_checkboxes(course_frame):
                logger.info("Handling multiple-choice question")
                indices = [int(num.strip()) for num in re.findall(r'\d+', answer) if num.strip().isdigit()]
                checkboxes = course_frame.locator("input[type='checkbox']").all()
                if not checkboxes:
                    logger.error("No checkboxes found for quiz question.")
                    return False
                
                for idx in indices:
                    if 0 < idx <= len(checkboxes):
                        try:
                            checkboxes[idx-1].check()
                            logger.info(f"Checked option {idx}")
                        except Exception as e:
                            logger.error(f"Failed to check option {idx}: {e}")
            else:
                logger.info("Handling text-based question")
                text_inputs = course_frame.locator("input[type='text'], textarea").all()
                if not text_inputs:
                    logger.error("No text input found for quiz question.")
                    return False
                try:
                    text_inputs[0].fill(answer)
                    logger.info(f"Filled text input with: {answer}")
                except Exception as e:
                    logger.error(f"Failed to fill text input: {e}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error handling quiz question: {e}")
            return False
    
    def handle_code_question(self, course_frame, page_content):
        """Handle coding questions"""
        try:
            code = self.get_code_answer(page_content)
            
            logger.info("Waiting for code editor to load (15 seconds)...")
            time.sleep(15)
            
            # Try to locate code editor (textarea or common editor classes)
            editor = course_frame.locator("textarea, .CodeMirror, .ace_editor, [contenteditable='true']").first
            if not editor:
                logger.error("No code editor found.")
                return False
            
            # Click to focus
            try:
                editor.click()
                logger.info("Clicked code editor")
            except Exception as e:
                logger.error(f"Failed to click code editor: {e}")
            
            time.sleep(1)
            self.page.keyboard.press("Control+a")
            time.sleep(0.5)
            self.page.keyboard.press("Delete")
            time.sleep(0.5)
            
            logger.info(f"Typing code ({len(code)} characters)")
            self.page.keyboard.type(code, delay=100)
            
            logger.info("Waiting 5 seconds before submitting...")
            time.sleep(5)
            
            submit_success = False
            for attempt in range(5):
                try:
                    if self.click_submit_or_next(course_frame, submit_mode=True):
                        logger.info(f"Successfully submitted code (attempt {attempt + 1})")
                        submit_success = True
                        break
                    time.sleep(3)
                except Exception as e:
                    logger.error(f"Error submitting code (attempt {attempt + 1}): {e}")
                    time.sleep(3)
            
            if not submit_success:
                logger.error("Failed to submit code after multiple attempts")
                return False
            
            logger.info("Waiting for submission feedback (30 seconds)...")
            time.sleep(30)
            
            next_success = False
            for attempt in range(5):
                try:
                    if self.click_submit_or_next(course_frame, submit_mode=False):
                        logger.info(f"Successfully clicked Next (attempt {attempt + 1})")
                        next_success = True
                        break
                    time.sleep(3)
                except Exception as e:
                    logger.error(f"Error clicking Next (attempt {attempt + 1}): {e}")
                    time.sleep(3)
            
            if not next_success:
                logger.error("Failed to click Next after multiple attempts")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error handling code question: {e}")
            return False
    
    def click_submit_or_next(self, course_frame, submit_mode=True):
        """Try to click submit/check/run buttons first, or next/continue if submit_mode=False"""
        submit_buttons = self.config.get('submit_buttons', [
            {"role": "button", "name": "Submit"},
            {"role": "button", "name": "Check Answer"},
            {"role": "button", "name": "Run"},
            {"role": "button", "name": "Execute"},
            {"role": "button", "name": "Verify"}
        ])
        next_buttons = self.config.get('next_buttons', [
            {"role": "button", "name": "Next"},
            {"role": "button", "name": "Continue"}
        ])
        button_texts = ["submit", "check", "run", "execute", "verify"] if submit_mode else ["next", "continue"]
        
        for attempt in range(3):
            try:
                buttons_to_try = submit_buttons if submit_mode else next_buttons
                for button_info in buttons_to_try:
                    try:
                        button = course_frame.get_by_role(button_info["role"], name=button_info["name"])
                        if button.count() > 0:
                            button.click()
                            logger.info(f"Clicked {button_info['name']} button (attempt {attempt + 1})")
                            return True
                    except Exception:
                        continue
                
                buttons = course_frame.locator("button").all()
                for button in buttons:
                    try:
                        button_text = button.inner_text().lower()
                        if any(text in button_text for text in button_texts):
                            button.click()
                            logger.info(f"Clicked button with text: {button_text} (attempt {attempt + 1})")
                            return True
                    except:
                        continue
                
                buttons = course_frame.locator("div[role='button']").all()
                for button in buttons:
                    try:
                        button_text = button.inner_text().lower()
                        if any(text in button_text for text in button_texts):
                            button.click()
                            logger.info(f"Clicked div button with text: {button_text} (attempt {attempt + 1})")
                            return True
                    except:
                        continue
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
            
        logger.error(f"No {'submit' if submit_mode else 'next'} button found after 3 attempts")
        return False
    
    def solve_quiz(self, course_frame):
        """Function to solve all questions in a quiz/exercise"""
        question_count = 0
        max_attempts = 20
        
        while question_count < max_attempts:
            question_count += 1
            logger.info(f"\n--- Processing question {question_count} ---")
            self.page.wait_for_timeout(500)
            
            try:
                course_frame = self.page.frame(self.config['course_frame'])
                if not course_frame:
                    logger.error("Lost course iframe reference!")
                    return question_count - 1
                    
                if not self.has_submit_button(course_frame):
                    logger.info("No submit button found. Quiz may be complete.")
                    return question_count - 1
                    
                page_text = course_frame.evaluate("() => document.body.innerText")
                logger.info(f"Text length: {len(page_text)} characters")
                
                if self.has_checkboxes(course_frame):
                    logger.info("Detected question type: Multiple choice")
                    if not self.handle_quiz_question(course_frame, page_text):
                        logger.error("Failed to handle quiz question.")
                        return question_count - 1
                elif self.has_code_editor(course_frame):
                    logger.info("Detected question type: Coding")
                    if not self.handle_code_question(course_frame, page_text):
                        logger.error("Failed to handle code question.")
                        return question_count - 1
                else:
                    logger.info("Detected question type: Text or SQL")
                    if not self.handle_quiz_question(course_frame, page_text):
                        logger.error("Failed to handle text/SQL question.")
                        return question_count - 1
                
                self.page.wait_for_timeout(200)
                
                logger.info("Attempting to submit answer...")
                if not self.click_submit_or_next(course_frame, submit_mode=True):
                    logger.error("Failed to submit answer. Quiz may be complete.")
                    return question_count
                
                self.page.wait_for_timeout(500)
                
                logger.info("Attempting to click Next...")
                next_found = self.click_submit_or_next(course_frame, submit_mode=False)
                if not next_found:
                    logger.error("No next/continue button found. Quiz may be complete.")
                    return question_count
                    
            except Exception as e:
                logger.error(f"Error processing question: {e}")
                break
            
            self.page.wait_for_timeout(2000)
        
        logger.info(f"Completed {question_count} questions")
        return question_count
    
    def go_back_to_contents(self, course_frame):
        """Go back to contents page using link or breadcrumb navigation"""
        try:
            contents_link = course_frame.get_by_role(self.config['back_to_contents']['role'], name=self.config['back_to_contents']['name'])
            if contents_link.count() > 0:
                contents_link.click()
                logger.info("Navigated back to Contents via link")
                time.sleep(3)
                return True
            
            breadcrumbs = course_frame.locator(".breadcrumb a").all()
            if breadcrumbs and len(breadcrumbs) > 0:
                breadcrumbs[0].click()
                logger.info("Navigated back via breadcrumb")
                time.sleep(3)
                return True
            
            links = course_frame.locator("a").all()
            for link in links:
                try:
                    link_text = link.inner_text().lower()
                    if "contents" in link_text or "home" in link_text:
                        link.click()
                        logger.info(f"Navigated back via link with text: {link_text}")
                        time.sleep(3)
                        return True
                except:
                    continue
            
            try:
                course_frame.evaluate("() => window.history.back()")
                logger.info("Used browser back function")
                time.sleep(3)
                
                current_url = course_frame.evaluate("() => window.location.href")
                if "quiz" in current_url.lower() or "assessment" in current_url.lower():
                    course_frame.evaluate("() => window.history.back()")
                    logger.info("Used browser back function again")
                    time.sleep(3)
                
                return True
            except Exception as e:
                logger.error(f"Browser back navigation failed: {e}")
            
            logger.error("Failed to navigate back to contents")
            return False
        except Exception as e:
            logger.error(f"Error going back to contents: {e}")
            return False
    
    def process_units(self, units):
        """Process all units and their subtopics with improved navigation and auto-unit transition"""
        course_frame = self.get_course_frame()
        if not course_frame:
            return False
        
        if not self.navigate_to_contents(course_frame):
            return False
        
        for unit_idx, unit in enumerate(units):
            logger.info(f"\n=== Processing {unit['name']} ===")
            
            if unit_idx == 0:
                unit_clicked = False
                for attempt in range(5):
                    time.sleep(5)
                    course_frame = self.get_course_frame()
                    if not course_frame:
                        logger.error("Lost course iframe reference!")
                        time.sleep(5)
                        continue
                    if self.click_button_containing_text(course_frame, unit["name"]):
                        logger.info(f"Clicked on unit: {unit['name']} (attempt {attempt + 1})")
                        unit_clicked = True
                        break
                    logger.error(f"Failed to click on unit: {unit['name']} (attempt {attempt + 1})")
                    time.sleep(5)
                
                if not unit_clicked:
                    logger.error(f"Failed to click on unit: {unit['name']} after multiple attempts")
                    continue
                
                time.sleep(10)
            else:
                logger.info(f"Assuming auto-navigation to {unit['name']}, skipping unit click")
                time.sleep(5)
            
            subtopics_completed = 0
            total_subtopics = len(unit["subtopics"])
            
            for idx, subtopic in enumerate(unit["subtopics"]):
                logger.info(f"\n-- Processing subtopic: {subtopic['name']} --")
                
                if idx == 0:
                    subtopic_clicked = False
                    for attempt in range(5):
                        course_frame = self.get_course_frame()
                        if not course_frame:
                            logger.error("Lost course iframe reference!")
                            time.sleep(5)
                            continue
                        if self.click_button_containing_text(course_frame, subtopic["name"]):
                            logger.info(f"Clicked on subtopic: {subtopic['name']} (attempt {attempt + 1})")
                            subtopic_clicked = True
                            break
                        logger.error(f"Failed to click on subtopic: {subtopic['name']} (attempt {attempt + 1})")
                        time.sleep(5)
                    
                    if not subtopic_clicked:
                        logger.error(f"Failed to click on subtopic: {subtopic['name']} after multiple attempts")
                        continue
                    
                    time.sleep(10)
                    
                    quiz_clicked = False
                    for attempt in range(5):
                        course_frame = self.get_course_frame()
                        if not course_frame:
                            logger.error("Lost course iframe reference!")
                            time.sleep(5)
                            continue
                        if self.click_button_containing_text(course_frame, subtopic["quiz"]):
                            logger.info(f"Clicked on quiz: {subtopic['quiz']} (attempt {attempt + 1})")
                            quiz_clicked = True
                            break
                        logger.error(f"Failed to click on quiz: {subtopic['quiz']} (attempt {attempt + 1})")
                        time.sleep(5)
                    
                    if not quiz_clicked:
                        logger.error(f"Failed to click on quiz: {subtopic['quiz']} after multiple attempts")
                        continue
                else:
                    quiz_clicked = False
                    for attempt in range(5):
                        course_frame = self.get_course_frame()
                        if not course_frame:
                            logger.error("Lost course iframe reference!")
                            time.sleep(5)
                            continue
                        if self.click_button_containing_text(course_frame, subtopic["quiz"]):
                            logger.info(f"Clicked on quiz: {subtopic['quiz']} (attempt {attempt + 1})")
                            quiz_clicked = True
                            break
                        logger.error(f"Failed to click on quiz: {subtopic['quiz']} (attempt {attempt + 1})")
                        time.sleep(5)
                    
                    if not quiz_clicked:
                        logger.error(f"Failed to click on quiz: {subtopic['quiz']} after multiple attempts")
                        continue
                
                time.sleep(10)
                
                questions_solved = self.solve_quiz(course_frame)
                logger.info(f"Completed {questions_solved} questions in {subtopic['name']}")
                
                subtopics_completed += 1
                logger.info(f"Subtopics completed: {subtopics_completed}/{total_subtopics}")
                
                time.sleep(5)
                
                if subtopics_completed < total_subtopics:
                    logger.info("Assuming auto-redirect to next subtopic's quiz list")
                    time.sleep(10)
                else:
                    logger.info("All subtopics in unit completed")
                    time.sleep(10)
                    break
        
        logger.info("\nAll units and subtopics processed.")
        return True
    
    def run(self):
        """Main method to run the automation"""
        if not self.login():
            return False
        
        course_name = self.config['course_name']
        if not self.navigate_to_course(course_name):
            return False
        
        self.process_units(self.config['units'])
        
        logger.info("Browser remains open for debugging")
        self.page.wait_for_timeout(3600000)
        
        return True

def main():
    """Main entry point"""
    if not EMAIL or not PASSWORD or not GROQ_API_KEY:
        logger.error("Missing required environment variables. Please set PLATFORM_EMAIL, PLATFORM_PASSWORD, and GROQ_API_KEY in .env file")
        return
    
    with sync_playwright() as playwright:
        automation = QuizAutomation(playwright, "config.json")
        automation.run()

if __name__ == "__main__":
    main()