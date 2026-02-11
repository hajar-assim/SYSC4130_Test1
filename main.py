#!/usr/bin/env python3
"""
Interactive CLI Quiz Application for SYSC4130
Uses arrow keys for navigation - just like a real interactive terminal app!
"""

import json
import os
import random
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import questionary
    from questionary import Style
except ImportError:
    print("Error: questionary library not found.")
    print("Please install it by running: pip install questionary")
    sys.exit(1)


# Custom style for the quiz
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # Question mark
    ('question', 'bold'),                # Question text
    ('answer', 'fg:#f44336 bold'),       # Selected answer
    ('pointer', 'fg:#673ab7 bold'),      # Pointer
    ('highlighted', 'fg:#673ab7 bold'),  # Highlighted choice
    ('selected', 'fg:#cc5454'),          # Selected choice
    ('separator', 'fg:#cc5454'),         # Separator
    ('instruction', 'fg:#858585'),       # Instructions
    ('text', ''),                        # Plain text
    ('disabled', 'fg:#858585 italic')    # Disabled choices
])


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(text: str, color=Colors.CYAN):
    """Print a formatted header."""
    print(f"\n{color}{Colors.BOLD}{'=' * 70}")
    print(f"{text.center(70)}")
    print(f"{'=' * 70}{Colors.ENDC}\n")


def print_separator(char='─', length=70, color=Colors.BLUE):
    """Print a separator line."""
    print(f"{color}{char * length}{Colors.ENDC}")


def print_success(text: str):
    """Print success message in green."""
    print(f"{Colors.GREEN}{Colors.BOLD}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message in red."""
    print(f"{Colors.RED}{Colors.BOLD}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message in cyan."""
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")


def print_progress_bar(current: int, total: int, bar_length: int = 40):
    """Print a progress bar."""
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    percentage = (current / total) * 100
    print(f"{Colors.CYAN}Progress: [{bar}] {current}/{total} ({percentage:.1f}%){Colors.ENDC}")


class QuizApp:
    def __init__(self, questions_dir: str = "questions"):
        self.questions_dir = Path(questions_dir)
        self.questions: List[Dict[str, Any]] = []
        self.score = 0
        self.total_questions = 0
        self.answered_questions = []

    def get_available_lectures(self) -> List[str]:
        """Get list of available lecture quiz files."""
        if not self.questions_dir.exists():
            return []

        json_files = list(self.questions_dir.glob("*.json"))
        return sorted([f.stem for f in json_files])

    def load_questions(self, lecture_name: str) -> bool:
        """Load questions from a specific lecture JSON file."""
        file_path = self.questions_dir / f"{lecture_name}.json"

        if not file_path.exists():
            print_error(f"{file_path} not found.")
            return False

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.questions.extend(data.get('questions', []))
            return True
        except json.JSONDecodeError:
            print_error(f"Invalid JSON in {file_path}")
            return False
        except Exception as e:
            print_error(f"Error loading {file_path}: {e}")
            return False

    def load_all_lectures(self):
        """Load questions from all available lecture files."""
        lectures = self.get_available_lectures()

        if not lectures:
            print_error("No lecture files found in the questions directory.")
            return False

        for lecture in lectures:
            self.load_questions(lecture)

        return len(self.questions) > 0

    def display_question_header(self, question_num: int):
        """Display question header with progress."""
        clear_screen()
        print_header(f"Question {question_num} of {self.total_questions}", Colors.CYAN)
        print_progress_bar(question_num - 1, self.total_questions)
        print()

    def ask_question(self, question: Dict[str, Any], question_num: int) -> Optional[int]:
        """Ask a question using interactive selection."""
        self.display_question_header(question_num)

        # Prepare choices with letters
        options = question['options']
        choices = [f"{chr(65 + i)}. {option}" for i, option in enumerate(options)]
        choices.append("❌ Quit Quiz")

        # Ask the question with arrow key selection
        answer = questionary.select(
            question['question'],
            choices=choices,
            style=custom_style,
            use_shortcuts=True,
            use_arrow_keys=True,
            instruction="(Use arrow keys to navigate, Enter to select)"
        ).ask()

        # Handle quit
        if answer is None or answer == "❌ Quit Quiz":
            return None

        # Extract the index from the answer (A. -> 0, B. -> 1, etc.)
        answer_index = ord(answer[0]) - 65
        return answer_index

    def check_answer(self, user_answer: int, correct_answer: int, explanation: str = None) -> bool:
        """Check if the answer is correct and provide feedback."""
        print()
        is_correct = user_answer == correct_answer

        if is_correct:
            print_success("Correct!")
            self.score += 1
        else:
            correct_letter = chr(65 + correct_answer)
            print_error(f"Incorrect. The correct answer was {correct_letter}.")

        if explanation:
            print(f"\n{Colors.CYAN}{Colors.BOLD}Explanation:{Colors.ENDC}")
            print(f"{Colors.CYAN}{explanation}{Colors.ENDC}")

        return is_correct

    def show_score(self, current_question: int):
        """Show current score."""
        percentage = (self.score / current_question) * 100 if current_question > 0 else 0
        print(f"\n{Colors.BOLD}Score: {self.score}/{current_question} ({percentage:.1f}%){Colors.ENDC}")

    def run_quiz(self):
        """Run the quiz with loaded questions."""
        if not self.questions:
            print_error("No questions loaded. Exiting.")
            return

        # Shuffle questions for variety
        random.shuffle(self.questions)
        self.total_questions = len(self.questions)

        clear_screen()
        print_header("🎯 QUIZ START 🎯", Colors.GREEN)
        print_info(f"Total Questions: {self.total_questions}")
        print_info("Use ↑↓ arrow keys to select your answer")
        print_info("Press Enter to confirm your selection")
        print_info("Select 'Quit Quiz' to exit at any time")

        questionary.press_any_key_to_continue(
            "\nPress any key to begin..."
        ).ask()

        for i, question in enumerate(self.questions, 1):
            user_answer = self.ask_question(question, i)

            if user_answer is None:
                print_info("\nQuiz interrupted by user.")
                break

            correct_answer = question['correct_answer']
            explanation = question.get('explanation', None)

            is_correct = self.check_answer(user_answer, correct_answer, explanation)

            # Store answer for review
            self.answered_questions.append({
                'question': question,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'question_num': i
            })

            self.show_score(i)

            # Pause between questions (except for the last one)
            if i < self.total_questions:
                questionary.press_any_key_to_continue(
                    f"\n{Colors.BOLD}Press any key to continue...{Colors.ENDC}"
                ).ask()

        self.show_final_results()

    def show_final_results(self):
        """Display final quiz results."""
        clear_screen()
        questions_answered = len(self.answered_questions)
        percentage = (self.score / questions_answered) * 100 if questions_answered > 0 else 0

        print_header("📊 QUIZ COMPLETE 📊", Colors.HEADER)

        print(f"{Colors.BOLD}Final Score: {self.score}/{questions_answered} ({percentage:.1f}%){Colors.ENDC}\n")

        # Performance feedback with color
        if percentage >= 90:
            print(f"{Colors.GREEN}{Colors.BOLD}🌟 Excellent work! You've mastered this material!{Colors.ENDC}")
        elif percentage >= 75:
            print(f"{Colors.GREEN}👍 Great job! You have a strong understanding!{Colors.ENDC}")
        elif percentage >= 60:
            print(f"{Colors.YELLOW}👌 Good effort! Keep practicing!{Colors.ENDC}")
        else:
            print(f"{Colors.RED}📚 Keep studying! Review the material and try again.{Colors.ENDC}")

        # Show breakdown
        correct_count = sum(1 for q in self.answered_questions if q['is_correct'])
        incorrect_count = questions_answered - correct_count

        print(f"\n{Colors.GREEN}✓ Correct: {correct_count}{Colors.ENDC}")
        print(f"{Colors.RED}✗ Incorrect: {incorrect_count}{Colors.ENDC}")

        # Offer review
        if incorrect_count > 0:
            print()
            review = questionary.confirm(
                "Would you like to review incorrect answers?",
                default=True,
                style=custom_style
            ).ask()

            if review:
                self.review_incorrect_answers()

    def review_incorrect_answers(self):
        """Review questions that were answered incorrectly."""
        incorrect = [q for q in self.answered_questions if not q['is_correct']]

        if not incorrect:
            print_success("You got all questions correct!")
            return

        clear_screen()
        print_header(f"📝 REVIEWING {len(incorrect)} INCORRECT ANSWERS", Colors.YELLOW)

        for idx, item in enumerate(incorrect, 1):
            question = item['question']
            user_ans = item['user_answer']
            correct_ans = item['correct_answer']

            print(f"\n{Colors.BOLD}Question {item['question_num']}:{Colors.ENDC}")
            print(f"{question['question']}\n")

            # Show options with indicators
            for i, option in enumerate(question['options']):
                letter = chr(65 + i)
                prefix = ""
                color = Colors.ENDC

                if i == user_ans:
                    prefix = f"✗ {letter}. (Your answer) "
                    color = Colors.RED
                elif i == correct_ans:
                    prefix = f"✓ {letter}. (Correct)    "
                    color = Colors.GREEN
                else:
                    prefix = f"  {letter}.              "

                print(f"{color}{prefix}{option}{Colors.ENDC}")

            # Show explanation
            if question.get('explanation'):
                print(f"\n{Colors.CYAN}{Colors.BOLD}Explanation:{Colors.ENDC}")
                print(f"{Colors.CYAN}{question['explanation']}{Colors.ENDC}")

            print_separator()

            if idx < len(incorrect):
                questionary.press_any_key_to_continue(
                    f"\n{Colors.BOLD}Press any key to continue...{Colors.ENDC}"
                ).ask()
                clear_screen()


def display_menu():
    """Display the main menu."""
    clear_screen()
    print_header("🎓 SYSC4130 Quiz Application 🎓", Colors.HEADER)
    print(f"{Colors.BOLD}Welcome to your interactive study tool!{Colors.ENDC}")
    print(f"{Colors.CYAN}Use arrow keys to navigate, Enter to select{Colors.ENDC}\n")


def select_lecture(quiz: QuizApp) -> bool:
    """Interactive lecture selection with arrow keys."""
    lectures = quiz.get_available_lectures()

    if not lectures:
        print_error("No lecture quiz files found in the 'questions' directory.")
        print_info("Please add JSON files with quiz questions first.")
        return False

    # Prepare choices
    choices = []
    for lecture in lectures:
        choices.append(lecture)
    choices.append("📚 All Lectures (Mixed)")
    choices.append("❌ Quit")

    # Ask user to select
    selection = questionary.select(
        "Select a lecture to quiz on:",
        choices=choices,
        style=custom_style,
        use_shortcuts=False,
        instruction="(Use ↑↓ arrow keys)"
    ).ask()

    # Handle selection
    if selection is None or selection == "❌ Quit":
        return False
    elif selection == "📚 All Lectures (Mixed)":
        print_info("Loading questions from all lectures...")
        quiz.load_all_lectures()
        return True
    else:
        print_info(f"Loading questions from: {selection}")
        quiz.load_questions(selection)
        return True


def main():
    """Main entry point for the quiz application."""
    try:
        display_menu()
        quiz = QuizApp()

        if not select_lecture(quiz):
            print_info("Goodbye! Good luck with your studies!")
            return

        # Run the quiz
        quiz.run_quiz()

        # Ask if user wants to take another quiz
        print()
        again = questionary.confirm(
            "Take another quiz?",
            default=False,
            style=custom_style
        ).ask()

        if again:
            main()
        else:
            clear_screen()
            print_header("👋 Thanks for studying!", Colors.GREEN)
            print_info("Good luck with your exam!")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Quiz interrupted. Goodbye!{Colors.ENDC}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
