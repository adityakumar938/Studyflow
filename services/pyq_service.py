from collections import Counter
from services.pdf_service import extract_text
from services.ai_service import extract_topics, extract_questions, map_questions_to_topics


class PYQService:
    def __init__(self, syllabus_pdf_path: str, pyq_pdf_path: str):
        self.syllabus_pdf_path = syllabus_pdf_path
        self.pyq_pdf_path = pyq_pdf_path
        self._cache = None  # (topics, questions, mapping) after first analysis

    def _analyse(self):
        """Run the 3 Gemini steps once, then reuse the result."""
        if self._cache is None:
            topics = extract_topics(extract_text(self.syllabus_pdf_path))
            questions = extract_questions(extract_text(self.pyq_pdf_path))
            mapping = map_questions_to_topics(questions, topics)
            self._cache = (topics, questions, mapping)
        return self._cache

    def get_topic_frequencies(self) -> dict:
        topics, questions, mapping = self._analyse()

        mapped_topics = []
        for qi, ti in mapping.items():
            if 0 <= ti < len(topics):
                t_obj = topics[ti]
                t_name = t_obj.get("name") or t_obj.get("topic")
                if t_name:
                    mapped_topics.append(t_name)

        return dict(Counter(mapped_topics))

    def get_unit_weightage(self) -> dict:
        topics, questions, mapping = self._analyse()

        unit_counts = Counter()
        for qi, ti in mapping.items():
            if 0 <= ti < len(topics):
                t_obj = topics[ti]
                unit = t_obj.get("unit")
                if unit:
                    unit_counts[unit] += 1

        return dict(unit_counts)