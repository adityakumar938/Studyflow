from services.pyq_service import PYQService

# Use your actual local PDF filenames
service = PYQService("syllabus.pdf", "pyq.pdf")

print("--- Topic Frequencies ---")
print(service.get_topic_frequencies())

print("\n--- Unit Weightages ---")
print(service.get_unit_weightage())