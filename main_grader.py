import json
from semantic_checker import SimilarityChecker
from feedback_marker import feedback_from_score, mark_from_score

def load_answers(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def grade_all(student_dict, teacher_dict, max_marks=10):
    checker = SimilarityChecker()
    results = {}
    total_marks = 0
    max_marks
    q_count = len(teacher_dict)
    for qno in teacher_dict:
        student_ans = student_dict.get(qno, "")
        teacher_ans = teacher_dict[qno]
        score,semantic,kw = checker.blended_score(student_ans, teacher_ans,semantic_weight=0.65,keyword_weight=0.35)
        marks = mark_from_score(score, max_marks)
        total_marks += marks
        feedback = feedback_from_score(score)
        results[qno] = {
            "student_ans": student_ans,
            "teacher_ans": teacher_ans,
            "score": score,
            "marks": marks,
            "feedback": feedback
        }
    percent = round((total_marks / (q_count * max_marks)) * 100, 2)
    return results, percent

if __name__ == "__main__":
    student_dict = load_answers("extracted_texts/student_parsed.json")
    teacher_dict = load_answers("extracted_texts/teacher_parsed.json")
    results, percent = grade_all(student_dict, teacher_dict)
    for qno, res in results.items():
        print(f"{qno}: {res['marks']}/10 | Similarity: {res['score']:.2f}")
        print(f"  Feedback: {res['feedback']}")
    print("\nTotal Score:", percent, "/100")
