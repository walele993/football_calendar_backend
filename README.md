# ⚽ Football Calendar Backend

*Automate football match data integration with Django and PostgreSQL, powered by pre-processed openfootball data.*

---

## 🚀 Introduction

**Football Calendar Backend** is a Django-based backend that fetches, processes, and stores football match data into a PostgreSQL database.  
Match data is sourced from **openfootball**, but pre-processed and cleaned via a custom pipeline in [**football_calendar_project**](https://github.com/walele993/football_calendar_project).

The backend is designed to serve **RESTful APIs** for use in frontend applications — especially **mobile apps** showing football fixtures in a calendar view.

---

## ✨ Key Features

- 🏆 **Matchday & Season Organization**: Matches are grouped by competition, season, and matchday.  
- 📅 **RESTful API Support**: Easily integrates with frontend clients via ready-to-use endpoints.  
- 🔄 **Scheduled Match Updates**: Automatically fetches and updates matches from your own JSON repository.  
- 🗂️ **Django + PostgreSQL Stack**: Robust and extensible backend foundation.  

---

## 🛋️ Installation

### Prerequisites

- Python 3.x  
- Django  
- PostgreSQL  
- `psycopg2` (for PostgreSQL integration)  
- `requests` (if needed for custom fetching)  

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

1. **Set Up the Database**  
   Update your PostgreSQL credentials in `settings.py` under the `DATABASES` section.

2. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

3. **Update Matches from GitHub JSON Repo**  
   Match data is pulled from `football_calendar_project`, already parsed into JSON format.  
   Run:

   ```bash
   python manage.py update_matches
   ```

4. **Run the Server**

   ```bash
   python manage.py runserver
   ```

5. **Consume the API**  
   REST endpoints (e.g., `/api/matches/`) expose match data to the frontend.  
   You can filter by date, league, or team.

---

## 🧠 Data Model

- **Match**
  - `home_team` / `away_team`: ForeignKeys to Team  
  - `date`: Match datetime  
  - `score_home` / `score_away`: Final score (nullable)  
  - `is_cancelled`: Boolean  
  - `matchday`: String or round name  
  - `league`: ForeignKey to League  
  - `season`: String (e.g., “2023/24”)  

- **Team**
  - `name`: Team name  

- **League**
  - `name`: League or competition name  

---

## ⚙️ API Overview

Example endpoints (depending on your URLs setup):

- `GET /api/matches/` – List all matches  
- `GET /api/matches/?date=2025-04-17` – Filter by date  
- `GET /api/matches/?league=UEFA Europa League` – Filter by league  
- `GET /api/teams/` – List of teams  
- `GET /api/leagues/` – List of leagues  

All endpoints return JSON, ready for mobile or web consumption.

---

## 🔁 Automatic Updates

This project includes a management command (`update_matches`) that clones your `football_calendar_project`,  
reads pre-parsed JSON files, and updates the database accordingly.

This can be scheduled daily via **GitHub Actions** or any other cron system.

---

## 🛠 Future Plans

- 📲 OAuth or token-based user auth for saving favorites  
- ⏰ Push notifications for upcoming fixtures  
- 📊 Stats & historical analysis per team  

---

## 🏅 Contribution

Feel free to contribute!

```bash
# Fork the repo
git clone https://github.com/your-username/football_calendar_backend.git
git checkout -b my-feature
```

Then open a Pull Request. All contributions are welcome!

---

## 👤 Credits

Developed by **Gabriele Meucci**  
Match data by **openfootball**, pre-processed in [**football_calendar_project**](https://github.com/walele993/football_calendar_project)
Deployed using [Render](https://render.com) for the PostgreSQL database  
and [Vercel](https://vercel.com) for hosting the RESTful API endpoints

---

*Power your football calendar apps with structured, clean data — all in one place!* ⚽🔥
