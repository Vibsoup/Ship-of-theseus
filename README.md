# Ship of Theseus Machine

A small Flask research prototype for studying how people judge identity through change. This first MVP collects anonymous scenario judgments and saves them to a local CSV file.

## Requirements

- Python 3.10+
- pip

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## What it currently does

- Lets a participant vary the percentage of ship components replaced.
- Captures continuity, appearance, history, function, identity rating, and an optional explanation.
- Validates submissions on the server and stores them in `data/responses.csv`.
- Displays a response count and provides a CSV export route.

## Data and privacy notes

- The app does not ask for a name, email, or demographic details.
- The CSV is stored on the machine running the app. It is excluded from Git by `.gitignore`.
- Do not deploy publicly or recruit research participants until consent language, data handling, security, and any institutional research-ethics requirements have been reviewed.
- This is a prototype, not a validated psychological instrument. A model trained on its responses would describe observed judgments, not determine objective identity.

## Next research steps

1. Define hypotheses and a preregistered experimental design.
2. Randomize scenario presentation and avoid changing multiple factors without recording them.
3. Add participant/session identifiers that preserve privacy while supporting repeated-measures analysis.
4. Establish a data dictionary and tests before training models.
5. Compare a simple baseline model with more flexible models using participant- and scenario-aware evaluation splits.
