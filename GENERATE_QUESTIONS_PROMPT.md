# AI Prompt for Generating Quiz Questions from Lecture PDFs

## Instructions for AI Assistant

You are tasked with creating comprehensive quiz questions from a course lecture PDF. Please read the attached PDF carefully and generate high-quality multiple-choice questions (MCQs) that test understanding of the material.

## Output Format

Generate your output as a valid JSON file with the following exact structure:

```json
{
  "lecture": "Lecture [NUMBER] - [TITLE]",
  "topic": "[Main topic or theme of the lecture]",
  "questions": [
    {
      "question": "[Question text here]",
      "options": [
        "[Option 1]",
        "[Option 2]",
        "[Option 3]",
        "[Option 4]"
      ],
      "correct_answer": [0-3],
      "explanation": "[Detailed explanation of why this answer is correct and why others are incorrect]"
    }
  ]
}
```

## Important Formatting Rules

1. **JSON Structure**:
   - Ensure valid JSON syntax (proper quotes, commas, brackets)
   - Use double quotes for all strings
   - `correct_answer` is a zero-based index (0 = first option, 1 = second option, etc.)

2. **Question Quality**:
   - Create 10-20 questions per lecture (adjust based on content density)
   - Mix difficulty levels: 40% easy, 40% medium, 20% hard
   - Cover all major topics and concepts from the lecture
   - Avoid ambiguous or trick questions

3. **Question Types to Include**:
   - **Conceptual Understanding**: Test comprehension of key ideas
   - **Application**: Apply concepts to scenarios
   - **Definitions**: Important terminology and definitions
   - **Calculations**: If applicable, include numerical problems
   - **Analysis**: Compare/contrast concepts or analyze situations

4. **Options Guidelines**:
   - Always provide exactly 4 options
   - Make all options plausible (avoid obviously wrong answers)
   - Ensure only one option is clearly correct
   - Vary the position of correct answers (don't always make it option A or D)
   - Keep options similar in length and complexity

5. **Explanations**:
   - Provide comprehensive explanations (2-4 sentences)
   - Explain WHY the correct answer is right
   - Optionally mention why common wrong answers are incorrect
   - Reference specific concepts or page numbers from the lecture when relevant

## Example Output

```json
{
  "lecture": "Lecture 3 - Digital Logic Design",
  "topic": "Boolean Algebra and Logic Gates",
  "questions": [
    {
      "question": "What is the output of an AND gate when both inputs are HIGH (1)?",
      "options": [
        "LOW (0)",
        "HIGH (1)",
        "Undefined",
        "Depends on the circuit"
      ],
      "correct_answer": 1,
      "explanation": "An AND gate outputs HIGH (1) only when both inputs are HIGH (1). This is the fundamental behavior of the AND operation in Boolean algebra, where 1 AND 1 = 1."
    },
    {
      "question": "Which Boolean law states that A + AB = A?",
      "options": [
        "Commutative Law",
        "Associative Law",
        "Absorption Law",
        "Distributive Law"
      ],
      "correct_answer": 2,
      "explanation": "The Absorption Law states that A + AB = A. This law allows us to simplify Boolean expressions by absorbing redundant terms. The term AB is absorbed by A because if A is true, the entire expression is true regardless of B."
    },
    {
      "question": "In a circuit diagram, what symbol represents a NOR gate?",
      "options": [
        "OR gate symbol with a bubble at the output",
        "AND gate symbol with bubbles at all inputs",
        "OR gate symbol with bubbles at all inputs",
        "AND gate symbol with a bubble at the output"
      ],
      "correct_answer": 0,
      "explanation": "A NOR gate is represented by an OR gate symbol with a small bubble (inversion circle) at the output. The bubble indicates negation, so NOR is the inverse of OR. This is a standard convention in digital logic circuit diagrams."
    }
  ]
}
```

## Quality Checklist

Before submitting, verify:
- [ ] Valid JSON syntax (test with a JSON validator)
- [ ] All questions have exactly 4 options
- [ ] All `correct_answer` values are between 0-3
- [ ] Each question has a meaningful explanation
- [ ] Questions cover diverse topics from the lecture
- [ ] No duplicate or nearly identical questions
- [ ] Options are free of typos and grammatical errors
- [ ] Questions are clear and unambiguous

## Usage Instructions

1. **Read the PDF**: Carefully review the entire lecture PDF
2. **Identify Key Topics**: Note the main concepts, formulas, definitions, and examples
3. **Generate Questions**: Create questions following the guidelines above
4. **Format as JSON**: Structure your output exactly as specified
5. **Save the File**: Save as `lecture[NUMBER]_[topic].json` in the `questions` folder
   - Example: `lecture3_digital_logic.json`

## Additional Tips

- Focus on testable knowledge that students should retain
- Include questions about important diagrams, charts, or figures if present
- For math/engineering courses, include worked examples and problem-solving questions
- Avoid questions that rely solely on memorization; test understanding when possible
- Keep question text concise but complete
- Ensure explanations add educational value, not just restate the answer

---

**Ready to generate questions?** Attach the lecture PDF and I'll create a comprehensive quiz file following this exact format.
