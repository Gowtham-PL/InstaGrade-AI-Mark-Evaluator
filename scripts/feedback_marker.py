def feedback_from_score(score):
    if score >= 0.85:
        return "Excellent answer! Meaning and keywords match almost perfectly."
    elif score >= 0.7:
        return "Nearly correct—minor gaps in meaning or facts."
    elif score >= 0.50:
        return "Partially correct—some important content missing."
    else:
        return "Weak answer; not matching expected concepts."

def mark_from_score(score, max_marks=10):
    return round(score * max_marks, 2)
