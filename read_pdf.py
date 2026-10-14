from pypdf import PdfReader

reader = PdfReader("syllabus.pdf")
print("Pages:", len(reader.pages))

text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

print(text)