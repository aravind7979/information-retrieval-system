import os
import PyPDF2

def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def read_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
        return ""

def load_documents(folder_path="documents"):
    docs = {}
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.endswith(".txt"):
            docs[filename] = read_txt(file_path)
        elif filename.endswith(".pdf"):
            docs[filename] = read_pdf(file_path)
            
    return docs
