# ⚽ Football Calendar Backend

*Automate football match data integration with Django and MongoDB, powered by pre-processed openfootball data.*

---

## 🚀 Introduction

**Football Calendar Backend** is a Django-based backend that fetches, processes, and stores football match data into a **MongoDB** database.
Match data is sourced from **openfootball**, but pre-processed and cleaned via a custom pipeline in [**football\_calendar\_project**](https://github.com/walele993/football_calendar_project).

The backend is designed to serve **RESTful APIs** for use in frontend applications — especially **mobile apps** showing football fixtures in a calendar view.

---

## ✨ Key Features

* 🏆 **Matchday & Season Organization**: Matches are grouped by competition, season, and matchday.
* 📅 **RESTful API Support**: Easily integrates with frontend clients via ready-to-use endpoints.
* 🔄 **Scheduled Match Updates**: Automatically fetches and updates matches from your own JSON repository.
* 🗂️ **Django + MongoDB Stack**: Robust and extensible backend foundation with MongoDB for better scalability and flexibility.

---

## 🛋️ Installation

### Prerequisites

* Python 3.x
* Django
* MongoDB (instead of PostgreSQL)
* `pymongo` (for MongoDB integration)
* `requests` (if needed for custom fetching)

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

1. **Set Up MongoDB**
   Update your MongoDB connection URI in `settings.py` under the `DATABASES` section.

2. **Apply Migrations**
   Since we’re using MongoDB, there are no traditional migrations. Ensure your MongoDB instance is properly configured.

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

* **Match**

  * `home_team` / `away_team`: Embedded document with team details
  * `date`: Match datetime
  * `score_home` / `score_away`: Final score (nullable)
  * `is_cancelled`: Boolean
  * `matchday`: String or round name
  * `league`: Embedded document with league details
  * `season`: String (e.g., “2023/24”)

* **Team**

  * `name`: Team name

* **League**

  * `name`: League or competition name

---

## ⚙️ API Overview

Example endpoints (depending on your URLs setup):

* `GET /api/matches/` – List all matches
* `GET /api/matches/?date=2025-04-17` – Filter by date
* `GET /api/matches/?league=UEFA Europa League` – Filter by league
* `GET /api/teams/` – List of teams
* `GET /api/leagues/` – List of leagues

All endpoints return JSON, ready for mobile or web consumption.

---

## 🔁 Automatic Updates

This project includes a management command (`update_matches`) that clones your `football_calendar_project`,
reads pre-parsed JSON files, and updates the MongoDB database accordingly.

This can be scheduled daily via **GitHub Actions** or any other cron system.

---

## ⚙️ Migration from PostgreSQL to MongoDB

As part of a strategic update to improve scalability and flexibility, we have transitioned from using PostgreSQL on Render to MongoDB for data storage and management. This change was made to support the growing needs of our application, providing better performance, especially when handling large volumes of data such as football matches, leagues, and teams.

### Key Changes:

* **Database:** The database backend has shifted from PostgreSQL (hosted on Render) to MongoDB. This allows us to take advantage of MongoDB’s flexibility with unstructured data and more efficient handling of large datasets.
* **Hosting:** We have removed Render from the stack, and MongoDB is now the primary database.
* **Performance Improvements:** MongoDB’s ability to handle large, unstructured data sets, as well as its indexing capabilities, provides faster queries, especially for complex filtering by date, team, and league.

---

## 🛠 Future Plans

* 📲 OAuth or token-based user auth for saving favorites
* ⏰ Push notifications for upcoming fixtures
* 📊 Stats & historical analysis per team

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
Match data by **openfootball**, pre-processed in [**football\_calendar\_project**](https://github.com/walele993/football_calendar_project); deployed using [MongoDB](https://www.mongodb.com) for the database and [Vercel](https://vercel.com) for hosting the RESTful API endpoints

---

*Power your football calendar apps with structured, clean data — all in one place!* ⚽🔥
