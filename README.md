# 📚 InstaGrade – AI Mark Evaluator

InstaGrade is an AI‑powered tool that automatically evaluates student answer sheets by comparing them with a teacher’s answer key.  
It reads PDFs, extracts text, splits it into question‑wise answers, and then scores each answer using **semantic similarity + keyword matching** so that students can write in their own words and still be graded fairly. ✨

---

## 🚀 Features

- 🔍 **PDF text extraction** using Azure Document Intelligence  
- ✂️ **Smart question parsing** (supports `1)`, `1.`, `Q1`, `Q1)`, etc.)  
- 🧠 **Semantic answer comparison** with Sentence Transformers  
- 🧾 **Hybrid scoring**: semantic similarity + keyword overlap  
- 📝 **Per‑question feedback** (correctness + comments)  
- 🎯 **Overall test score (0–100)**  
- 🌐 **Pluggable frontend** (web UI planned / in progress)

---

## 🏗️ Architecture Overview

Backend is split into small, focused modules:

- `extract_text.py` – Extracts raw text from student & teacher PDFs and saves JSON  
- `parse_questions_improved.py` – Converts raw text into `{Q1: answer, Q2: answer, ...}` dictionaries  
- `similarity_checker.py` – Cleans text and computes semantic + keyword scores  
- `feedback_marker.py` – Converts scores into marks and human‑readable feedback  
- `main.py` – Orchestrates the entire pipeline (extract → parse → grade)  
- `extracted_texts/` – Stores intermediate and final JSON files

A separate **frontend** (e.g., React/Next.js) can call backend APIs to:
- upload PDFs,
- trigger the grading pipeline,
- display question‑wise breakdown, feedback, and total score.

