import json
import random
from pathlib import Path

def shuffle_question_options(question):
    """Shuffle the options for a single question while maintaining correct answer tracking."""
    options = question['options']
    correct_index = question['correct_answer']
    correct_answer_text = options[correct_index]

    # Shuffle the options
    random.shuffle(options)

    # Find the new index of the correct answer
    new_correct_index = options.index(correct_answer_text)

    # Update the question
    question['options'] = options
    question['correct_answer'] = new_correct_index

    return question

def shuffle_lecture_file(file_path):
    """Shuffle all questions in a lecture file."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Shuffle each question's options
    for question in data['questions']:
        shuffle_question_options(question)

    # Write back to file with proper formatting
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Shuffled answers in {file_path.name}")

def main():
    # Find all lecture JSON files
    questions_dir = Path('/Users/hajarassim/Documents/school/Winter 2026/SYSC4130/test/questions')
    lecture_files = list(questions_dir.glob('lecture*.json'))

    print(f"Found {len(lecture_files)} lecture files to process")

    for file_path in lecture_files:
        shuffle_lecture_file(file_path)

    print("Done! All answers have been shuffled.")

if __name__ == '__main__':
    main()
