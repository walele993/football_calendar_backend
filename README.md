# ⚽ Football Calendar Backend

*Automate football match data extraction and populate a database with Django for various leagues!*  

---

## 🚀 Introduction

**Football Calendar Backend** is a Django-based backend project designed to fetch football match data, process it, and store it in a PostgreSQL database. The project extracts match data from a public JSON file, organizes it by matchdays, and tracks match results. This backend is ready for integration with frontend applications that require real-time football match data.

### Key Features
- 🏆 **Matchday Organization**: Automatically organizes match results by competition, season, and matchday.
- 📅 **Comprehensive Calendar**: Supports multiple leagues and seasons, handling matchups, times, and results.
- 🔄 **Automatic Data Fetching**: Fetches match data from a public JSON file and updates the database.
- 🗂️ **Easy Backend Integration**: Uses Django and PostgreSQL, offering a clean structure for further application development.

---

## 🛋️ Installation

### Prerequisites
- Python 3.x
- Django
- psycopg2 (for PostgreSQL integration)
- Requests (for fetching data)

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

1. **Set Up the Database**:  
   First, configure the `DATABASES` setting in `settings.py` with your PostgreSQL credentials.

2. **Apply Database Migrations**:  
   Run the following command to set up your database schema:
   ```bash
   python manage.py migrate
   ```

3. **Fetch and Update Matches**:  
   To fetch the latest match data from the public JSON file and update the database:
   ```bash
   python manage.py fetch_matches
   ```

4. **Run the Development Server**:  
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```

5. **Access Match Data**:  
   Once the data is fetched, you can query the database for match information or expose it via Django REST APIs for frontend applications.

---

## 🧠 Data Structure

The database will store match data in tables with the following key fields:

- **Match**:
  - `home_team`: ForeignKey to the Team model.
  - `away_team`: ForeignKey to the Team model.
  - `date`: DateTime field for match date and time.
  - `score_home`: Integer for home team score.
  - `score_away`: Integer for away team score.
  - `competition`: String for competition name (e.g., English Premier League).
  - `season`: String for the season (e.g., 2023/24).

- **Team**:
  - `name`: Name of the football team (e.g., Manchester United).
  - `country`: Country of the team (e.g., England).

---

## 📝 Key Functions

### ✨ Data Extraction & Processing
- **`fetch_and_update_matches()`** → Fetches the latest match data from a JSON source, processes it, and updates the database with the latest results.
- **`get_or_create_teams()`** → Fetches or creates teams in the database based on the match data.

### 🗃️ Database Management
- The backend handles automatic database updates, ensuring data is synchronized with the latest match results.
- The system checks for existing matches and updates them if the data has changed (e.g., updated score, match time).

---

## 💪 Future Enhancements

- 🌍 **Expand League Support**: Add support for more football leagues and competitions.
- 📅 **Match Reminders**: Integrate match reminders for upcoming fixtures.
- 📝 **Match Analytics**: Implement match summaries and team performance analysis.

---

## 🏅 Contribution

This is a **work-in-progress** project, and contributions are welcome!  

1. **Fork** the repository  
2. **Clone** your fork:  
   ```bash
   git clone https://github.com/your-username/football_calendar_backend.git
   ```
3. Create a **feature branch**:  
   ```bash
   git checkout -b feature-enhancement
   ```
4. **Push** changes & submit a **pull request**

---

## 🏁 Credits

Project created by **Gabriele Meucci**.  

Data sourced from publicly available football match fixtures in JSON format.

---

*Ready to manage and organize football match data in the easiest way possible? Let’s get started!* ⚽🔥