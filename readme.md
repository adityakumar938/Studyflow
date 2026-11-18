# StudyFlow — Adaptive Academic Planning & PYQ Intelligence

CSE-AI semester mini-project. Gemini reads a syllabus PDF and a previous-year
paper, maps every question to its topic, and allocates study hours by real
exam weightage. Served as a FastAPI app with a Jinja2 + Bootstrap web UI.

## Run
1. `python -m venv .venv` and activate it
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and set `GEMINI_API_KEY`
4. From the repo root: `uvicorn main:app --reload`
5. Open http://127.0.0.1:8000 (API docs at /docs)

Swap `syllabus.pdf` / `pyq.pdf` in the root for your own documents
(keep the filenames; text-based PDFs only, not scans).

## Endpoints
| Route | Returns |
|---|---|
| `/` | Homepage (HTML) |
| `/dashboard` | Live dashboard (HTML) |
| `/api` | API index (JSON) |
| `/weightages` | `{unit: question_count}` |
| `/frequencies` | `{topic: appearance_count}` |
| `/plan?hours=N` | `{unit: {questions_appeared, weightage_percentage, recommended_hours}}` |
| `/export-pdf?hours=N` | PDF report |

## Team status
- Member 3 — AI services + JSON API: live (`services/`)
- Member 2 — Web UI: live (`templates/`, `static/`)
- Member 1 — Database/auth/subjects layer: not in repo yet (needed for
  login, uploads, exam dates, progress, Crisis Mode)

## Known issues (handoff)
- `pyq_service.py`: `enumerate(mapping)` should be `mapping.items()` (both methods)
- No caching: each API call re-runs 3 Gemini calls; add a per-instance cache
- `ai_service.py` hardcodes the model and ignores `GEMINI_MODEL` from `.env`
- Delete empty stray file `services/report_service.py.txt`