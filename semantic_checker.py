from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def keyword_score(student, teacher):
    student_words = set(student.split())
    teacher_words = set(teacher.split())
    return len(student_words & teacher_words) / max(1, len(teacher_words))

class SimilarityChecker:
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2')

    def blended_score(self, student_ans, teacher_ans, semantic_weight=0.7, keyword_weight=0.3):
        s_clean = clean_text(student_ans)
        t_clean = clean_text(teacher_ans)
        embeddings = self.model.encode([s_clean, t_clean])
        semantic = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
        kw = keyword_score(s_clean, t_clean)
        score = semantic_weight * semantic + keyword_weight * kw
        return score, semantic, kw
