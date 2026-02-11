# 🎓 SYSC4130 Interactive Quiz Application

An interactive CLI quiz application with **arrow key navigation** for studying SYSC4130 course material.

## ✨ Features

- **🎯 Arrow Key Navigation** - Use ↑↓ keys to select answers (no typing numbers!)
- **📊 Progress Tracking** - Visual progress bar showing quiz completion
- **🎨 Color-Coded Feedback** - Green for correct, red for incorrect answers
- **📝 Review Mode** - Review all incorrect answers after completing the quiz
- **🔄 Multiple Lectures** - Choose individual lectures or mix all lectures
- **💾 Detailed Explanations** - Learn from comprehensive answer explanations

## 🚀 Installation

1. **Install the required dependency:**
   ```bash
   pip install questionary
   ```

   Or using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

1. **Run the quiz application:**
   ```bash
   python main.py
   ```

2. **Navigate the quiz:**
   - Use **↑** and **↓** arrow keys to highlight your answer
   - Press **Enter** to select
   - Press any key to continue between questions
   - Select "Quit Quiz" to exit at any time

3. **After completing the quiz:**
   - View your score and performance feedback
   - Choose to review incorrect answers
   - Option to take another quiz

## 📁 Project Structure

```
test/
├── main.py              # Main quiz application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── questions/          # Quiz questions folder
    ├── lecture1.json   # Lecture 1 questions
    ├── lecture2.json   # Lecture 2 questions
    ├── lecture3.json   # Lecture 3 questions
    └── lecture4.json   # Lecture 4 questions
```

## 📝 Question Format

Questions are stored in JSON format:

```json
{
  "lecture": "Lecture X - Topic",
  "topic": "Topic Name",
  "questions": [
    {
      "question": "Question text here?",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": 0,
      "explanation": "Explanation of the correct answer"
    }
  ]
}
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| ↑ / ↓ | Navigate options |
| Enter | Select answer |
| Any Key | Continue to next question |
| Ctrl+C | Quit application |

## 📚 Quiz Content

The quiz covers:
- **Lecture 1**: HCI Fundamentals, Universal Design, Usability Goals, Design Principles
- **Lecture 2**: Heuristic Evaluation, Cognitive Walkthrough, Nielsen's 10 Usability Heuristics
- **Lecture 3**: Data Gathering Methods (Interviews, Surveys, Observation, Usability Testing)
- **Lecture 4**: Data Analysis (Qualitative & Quantitative Methods, Statistics)

## 🌟 Example Quiz Flow

```
🎓 SYSC4130 Quiz Application 🎓
======================================================================

? Select a lecture to quiz on: (Use ↑↓ arrow keys)
  lecture1
  lecture2
  lecture3
  lecture4
❯ 📚 All Lectures (Mixed)
  ❌ Quit

? What does the 'Consistency and Standards' heuristic require? (Use arrow keys to navigate, Enter to select)
  A. Using unique design patterns for each page to keep users engaged
❯ B. Users should not have to wonder whether different words, situations, or actions mean the same thing
  C. All interfaces should look identical across all platforms
  D. Following only internal company standards, not industry conventions
  ❌ Quit Quiz

✓ Correct!

Explanation: The Consistency and Standards heuristic states that users should not have to wonder...
```

## 💡 Tips for Best Experience

- Run in a terminal with color support for best visual experience
- Use a terminal size of at least 80 columns wide
- Questions are shuffled each time for variety
- Review mode helps reinforce learning after the quiz

## 🛠️ Troubleshooting

**Issue**: `questionary` not found
**Solution**: Run `pip install questionary`

**Issue**: Colors not displaying correctly
**Solution**: Ensure your terminal supports ANSI colors

**Issue**: Arrow keys not working
**Solution**: Try running in a different terminal (iTerm2, Terminal.app, etc.)

---

AI-generated questions for HCI test prep.
Created for SYSC4130 Winter 2026
