#!/usr/bin/env python3
"""
CLI Quiz Application for SYSC4130
Loads questions from JSON files and provides an interactive quiz experience.
"""

import json
import os
import random
from pathlib import Path
from typing import List, Dict, Any


class QuizApp:
    def __init__(self, questions_dir: str = "questions"):
        self.questions_dir = Path(questions_dir)
        self.questions: List[Dict[str, Any]] = []
        self.score = 0
        self.total_questions = 0

    def get_available_lectures(self) -> List[str]:
        """Get list of available lecture quiz files."""
        if not self.questions_dir.exists():
            return []

        json_files = list(self.questions_dir.glob("*.json"))
        return [f.stem for f in json_files]

    def load_questions(self, lecture_name: str) -> bool:
        """Load questions from a specific lecture JSON file."""
        file_path = self.questions_dir / f"{lecture_name}.json"

        if not file_path.exists():
            print(f"Error: {file_path} not found.")
            return False

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.questions.extend(data.get('questions', []))
            return True
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {file_path}")
            return False
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return False

    def load_all_lectures(self):
        """Load questions from all available lecture files."""
        lectures = self.get_available_lectures()

        if not lectures:
            print("No lecture files found in the questions directory.")
            return False

        for lecture in lectures:
            self.load_questions(lecture)

        return len(self.questions) > 0

    def display_question(self, question: Dict[str, Any], question_num: int):
        """Display a single question with its options."""
        print(f"\n{'=' * 60}")
        print(f"Question {question_num}/{self.total_questions}")
        print(f"{'=' * 60}")
        print(f"\n{question['question']}\n")

        options = question['options']
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

    def get_user_answer(self, num_options: int) -> int:
        """Get and validate user's answer."""
        while True:
            try:
                answer = input(f"\nYour answer (1-{num_options}): ").strip()
                answer_num = int(answer)

                if 1 <= answer_num <= num_options:
                    return answer_num - 1  # Convert to 0-based index
                else:
                    print(f"Please enter a number between 1 and {num_options}.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nQuiz interrupted by user.")
                exit(0)

    def check_answer(self, user_answer: int, correct_answer: int, explanation: str = None):
        """Check if the answer is correct and provide feedback."""
        if user_answer == correct_answer:
            print("\n✓ Correct!")
            self.score += 1
        else:
            print(f"\n✗ Incorrect. The correct answer was option {correct_answer + 1}.")

        if explanation:
            print(f"\nExplanation: {explanation}")

    def run_quiz(self):
        """Run the quiz with loaded questions."""
        if not self.questions:
            print("No questions loaded. Exiting.")
            return

        # Shuffle questions for variety
        random.shuffle(self.questions)
        self.total_questions = len(self.questions)

        print(f"\n🎯 Starting quiz with {self.total_questions} questions!\n")

        for i, question in enumerate(self.questions, 1):
            self.display_question(question, i)

            num_options = len(question['options'])
            user_answer = self.get_user_answer(num_options)

            correct_answer = question['correct_answer']
            explanation = question.get('explanation', None)

            self.check_answer(user_answer, correct_answer, explanation)

            # Show current score
            print(f"\nCurrent Score: {self.score}/{i}")

            # Pause between questions (except for the last one)
            if i < self.total_questions:
                input("\nPress Enter to continue...")

        self.show_final_results()

    def show_final_results(self):
        """Display final quiz results."""
        percentage = (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0

        print(f"\n{'=' * 60}")
        print("QUIZ COMPLETE!")
        print(f"{'=' * 60}")
        print(f"\nFinal Score: {self.score}/{self.total_questions} ({percentage:.1f}%)")

        if percentage >= 90:
            print("🌟 Excellent work!")
        elif percentage >= 75:
            print("👍 Great job!")
        elif percentage >= 60:
            print("👌 Good effort!")
        else:
            print("📚 Keep studying!")
        print()


def main():
    """Main entry point for the quiz application."""
    print("=" * 60)
    print("SYSC4130 Quiz Application")
    print("=" * 60)

    quiz = QuizApp()
    lectures = quiz.get_available_lectures()

    if not lectures:
        print("\nNo lecture quiz files found in the 'questions' directory.")
        print("Please add JSON files with quiz questions first.")
        return

    print("\nAvailable lectures:")
    for i, lecture in enumerate(lectures, 1):
        print(f"{i}. {lecture}")
    print(f"{len(lectures) + 1}. All lectures")

    # Get user selection
    while True:
        try:
            choice = input(f"\nSelect a lecture (1-{len(lectures) + 1}): ").strip()
            choice_num = int(choice)

            if 1 <= choice_num <= len(lectures):
                # Load specific lecture
                lecture_name = lectures[choice_num - 1]
                print(f"\nLoading questions from: {lecture_name}")
                quiz.load_questions(lecture_name)
                break
            elif choice_num == len(lectures) + 1:
                # Load all lectures
                print("\nLoading questions from all lectures...")
                quiz.load_all_lectures()
                break
            else:
                print(f"Please enter a number between 1 and {len(lectures) + 1}.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            return

    # Run the quiz
    quiz.run_quiz()


if __name__ == "__main__":
    main()
