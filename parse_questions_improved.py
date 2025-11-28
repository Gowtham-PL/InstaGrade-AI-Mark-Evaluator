import json
import re
import os

def clean_text(text):
    """
    Clean and normalize text for semantic grading.
    - Lowercase
    - Remove punctuation
    - Remove excess spaces
    - Remove special characters
    """
    # Lowercase
    text = text.lower()
    # Remove non-letter characters
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Strip whitespace
    return text.strip()

def clean_dict(ans_dict):
    """Return a dict where every answer is cleaned"""
    return {q: clean_text(ans) for q, ans in ans_dict.items()}
def parse_questions_flexible(json_path, output_format='dict'):
    """
    Parse questions from extracted text JSON with flexible delimiter patterns.
    
    Supported delimiters:
    - Q1, q1, Q 1, q 1
    - 1), 2), 3)
    - 1., 2., 3.
    - 1:, 2:, 3:
    - Q1), Q2), Q3)
    - Q1., Q2., Q3.
    
    Args:
        json_path: Path to the extracted JSON file or dictionary
        output_format: 'dict' for {Q1: answer, Q2: answer} or 'list' for list format
    
    Returns:
        Dictionary with question numbers as keys and answers as values
    """
    # Load text from file or dict
    if isinstance(json_path, str):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        full_text = data.get('text', '')
    elif isinstance(json_path, dict):
        full_text = json_path.get('text', '')
    else:
        raise ValueError("Input must be a file path or dictionary")
    
    # Enhanced regex pattern to match all question number formats
    # Matches: Q1, q1, Q1), Q1., 1), 1., etc.
    pattern = r'(?:^|\n|\s)([Qq]?\s*\d+\s*[\).:])'
    
    # Find all matches with their positions
    matches = list(re.finditer(pattern, full_text))
    
    if not matches:
        print("⚠ Warning: No question delimiters found. Returning entire text as Q1.")
        return {"Q1": clean_text(full_text)}
    
    questions = {}
    
    for i, match in enumerate(matches):
        # Extract question marker
        question_marker = match.group(1).strip()
        
        # Extract numeric value
        q_num = re.search(r'\d+', question_marker)
        if q_num:
            question_key = f"Q{q_num.group()}"
        else:
            question_key = f"Q{i+1}"
        
        # Find start position (after the question marker)
        start_pos = match.end()
        
        # Find end position (next question or end of text)
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(full_text)
        
        # Extract and clean answer text
        answer_text = full_text[start_pos:end_pos].strip()
        answer_text = clean_text(answer_text)
        
        # Only add non-empty answers
        if answer_text:
            questions[question_key] = answer_text
    
    return questions

def clean_text(text):
    """
    Clean and normalize text.
    
    Args:
        text: Raw text string
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace (multiple spaces, tabs, newlines)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove any remaining special formatting characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    return text

def save_parsed_questions(questions_dict, output_path):
    """
    Save parsed questions to JSON file.
    
    Args:
        questions_dict: Dictionary of parsed questions
        output_path: Path to save JSON file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions_dict, f, ensure_ascii=False, indent=4)
    
    print(f"✓ Parsed questions saved to {output_path}")
    print(f"  Total questions found: {len(questions_dict)}")

def parse_both_files(student_json="extracted_texts/student_raw.json", 
                     teacher_json="extracted_texts/teacher_raw.json"):
    """
    Parse both student and teacher answer files.
    
    Args:
        student_json: Path to student extracted text JSON
        teacher_json: Path to teacher extracted text JSON
    
    Returns:
        Tuple of (student_questions, teacher_questions)
    """
    print("\n" + "="*70)
    print("PARSING EXTRACTED TEXTS")
    print("="*70 + "\n")
    
    # Parse student answers
    print("📄 Parsing student answers...")
    try:
        student_questions = parse_questions_flexible(student_json)
        save_parsed_questions(student_questions, "extracted_texts/student_parsed.json")
    except FileNotFoundError:
        print(f"❌ Error: {student_json} not found!")
        student_questions = {}
    
    print()
    
    # Parse teacher answers
    print("📋 Parsing teacher answer key...")
    try:
        teacher_questions = parse_questions_flexible(teacher_json)
        save_parsed_questions(teacher_questions, "extracted_texts/teacher_parsed.json")
    except FileNotFoundError:
        print(f"❌ Error: {teacher_json} not found!")
        teacher_questions = {}
    
    print("\n" + "="*70)
    print("PARSING COMPLETE")
    print("="*70)
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Student answers: {len(student_questions)} questions")
    print(f"   Teacher answers: {len(teacher_questions)} questions")
    
    # Check for mismatches
    if len(student_questions) != len(teacher_questions):
        print(f"\n⚠ Warning: Number of questions don't match!")
    
    return student_questions, teacher_questions

if __name__ == "__main__":
    # Parse both files
    student_q, teacher_q = parse_both_files()
    
    # Display preview
    print("\n" + "-"*70)
    print("PREVIEW (First 2 questions):")
    print("-"*70)
    
    for i, (q_num, answer) in enumerate(list(student_q.items())[:2]):
        print(f"\n{q_num}: {answer[:100]}..." if len(answer) > 100 else f"\n{q_num}: {answer}")
