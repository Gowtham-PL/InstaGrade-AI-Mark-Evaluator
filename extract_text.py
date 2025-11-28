import os
import json
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()
endpoint = os.getenv("AZURE_FORMRECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORMRECOGNIZER_KEY")

# Azure client setup
client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def extract_full_text(pdf_path, output_filename=None):
    """
    Extract full text from a PDF as a single string and save it to a JSON file.
    """
    with open(pdf_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", document=f)
        result = poller.result()

    all_text = []
    for page in result.pages:
        page_text = " ".join([line.content for line in page.lines])
        all_text.append(page_text)

    full_text = "\n".join(all_text)

    # Create folder
    os.makedirs("extracted_texts", exist_ok=True)

    # Use default name if none given
    if output_filename is None:
        output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".json"

    output_path = os.path.join("extracted_texts", output_filename)

    # Save as JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"text": full_text}, f, ensure_ascii=False, indent=4)

    print(f" Extracted text saved to {output_path}")
    return full_text


if __name__ == "__main__":
    student_pdf = "sample_pdfs/student.pdf"
    teacher_pdf = "sample_pdfs/teacher.pdf"

    extract_full_text(student_pdf, "student_raw.json")
    extract_full_text(teacher_pdf, "teacher_raw.json")
