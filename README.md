# Golf Stats App

A Flask web app for golfers around Cork to log their rounds, calculate a handicap differential for each round, track putting statistics over time, and compare scores on per-course leaderboards.

Built as part of a university web development module.

---

## Features

These are the features implemented in `app.py` and `forms.py`:

- **Accounts:** register and log in with a user ID and password. Passwords are stored as salted hashes (Werkzeug's `generate_password_hash`), and pages that need a login redirect to `/login`.
- **Enter a round** (`/enter_round`): pick one of 9 Cork-area courses and enter your score, date and four putting stats:
  - putts per round
  - one-putt %
  - three-putt avoidance
  - average distance of putts made
- **Handicap differential:** each round's differential is calculated as `(score − course rating) × 113 / slope rating`. Course and slope ratings are hard-coded per course.
- **Round history** (`/round_history`): your rounds (course, date, score, differential) between two dates.
- **Putting stats chart** (`/stats`): a matplotlib radar chart comparing your average putting stats with a fixed set of reference values (labelled "Maverick").
- **Course leaderboards** (`/leaderboard`): all recorded rounds on a chosen course, lowest score first.
- **Update or delete a round** (`/update`, `/delete`): edit or remove a round by its date.

## Tech stack

- **Backend:** Python, Flask, Flask-Session (filesystem sessions), Flask-WTF / WTForms (forms and validation)
- **Database:** SQLite via Python's built-in `sqlite3`
- **Charts:** matplotlib (Agg backend) and NumPy
- **Frontend:** Jinja2 templates (see the note below)

## Project structure

```
Golf-Stats-App/
├── app.py            # Flask app: config, auth, all routes and handicap/stats logic
├── database.py       # SQLite connection helpers (get_db / close_db), DB path = ./app.db
├── forms.py          # Flask-WTF form classes for each page
├── schema.sql        # Creates the users, rounds and putting_stats tables
├── test.sql          # Scratch query used during development
├── run.py            # CGI entry point used to host the app on the university web server
├── .flaskenv         # FLASK_APP / FLASK_DEBUG for `flask run`
├── requirements.txt
└── README.md
```

> **Note:** `app.py` renders Jinja templates (`index.html`, `login.html`, `register.html`, `enterRound.html`, `stats.html`, `roundHistory.html`, `leaderboard.html`, `delete.html`, `update.html`) from a `templates/` folder, and writes the chart to `static/plot.png`. Those `templates/` and `static/` folders are **not in this repository yet**. Until they are added, the backend starts but every page returns a `TemplateNotFound` error.

## Getting started

Tested with Python 3.13 on Linux.

```bash
git clone https://github.com/Darragh7/Golf-Stats-App.git
cd Golf-Stats-App

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create the local SQLite database from the schema
python -c "import sqlite3; c = sqlite3.connect('app.db'); c.executescript(open('schema.sql').read()); c.commit()"

# The stats page saves its chart here
mkdir -p static

flask run                        # reads FLASK_APP=app.py from .flaskenv
```

Then open http://127.0.0.1:5000.

`schema.sql` starts with `DROP TABLE IF EXISTS`, so re-running the database command wipes all existing data.

## Data model

Defined in `schema.sql`:

| Table | Columns | Purpose |
|---|---|---|
| `users` | `user_id` (PK, text), `password` (hashed) | Accounts |
| `rounds` | `id` (PK), `user_id`, `date`, `name` (course), `score`, `handicap` | One row per round, with its handicap differential |
| `putting_stats` | `id` (PK), `user_id`, `date`, `puts_per_round`, `one_putt_percent`, `three_putt_avoid`, `avg_putt_dist` | Putting stats entered with each round |

Course and slope ratings live in a dictionary in `app.py`, not in the database.

## Future work

- Add the `templates/` and `static/` folders so the UI can be run from a fresh clone
- Read `SECRET_KEY` from an environment variable rather than hard-coding it in `app.py`
- Make sure update, delete and stats only touch the logged-in user's rows, and use the chosen end date in the stats query
- Calculate a full handicap index from recent differentials, not just per-round differentials
- Move course and slope ratings into a database table
- Add automated tests

## Author

**Darragh O'Keeffe**: [darragh7.github.io](https://darragh7.github.io) · [GitHub @Darragh7](https://github.com/Darragh7)
