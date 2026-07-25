# Kibaii Django Tournament Runner

A Django-based football (soccer) tournament management system that simulates an English Premier League-style competition with role-based access control for fans, coaches, and officials.

## What this is

**Kibaii** is a Django web application designed to manage and simulate football tournaments. It allows officials to create and manage matches, coaches to build team rosters and set lineups, and fans to view league standings and match fixtures. The system tracks comprehensive team statistics (wins, draws, losses, goals) and provides role-based access to different features.

### Stack
- **Language:** Python (67.3%) + HTML (32.7%)
- **Framework:** Django 5.2.7
- **Database:** SQLite (db.sqlite3)
- **Authentication:** Django custom user model with role-based permissions

## How it's organized

```
kibaii_django-tournament-runner/
├── tournament_runner/           Django project configuration
│   ├── settings.py             Project settings (apps, middleware, DB config)
│   ├── urls.py                 Main URL router
│   ├── wsgi.py & asgi.py      Application entry points
│   └── __init__.py
├── league/                     Core tournament management app
│   ├── models.py              Team, Match, Player, StartingEleven, Substitutes
│   ├── views.py               League table, matchdays, match CRUD, lineup management
│   ├── urls.py                League endpoints (league table, matches, lineups)
│   ├── admin.py               Django admin registration
│   ├── forms.py               Player forms
│   ├── match_forms.py         Match result submission form
│   ├── lineup_forms.py        Starting eleven & substitutes forms
│   ├── management/
│   │   └── commands/
│   │       ├── seed_teams.py      Initialize 20 teams
│   │       └── simulate_tournament.py  Generate & simulate matches
│   ├── templates/league/      HTML templates for views
│   └── migrations/            Database schema changes
├── users/                      User authentication & roles
│   ├── models.py              CustomUser (fan/coach/official)
│   ├── views.py               User profile, registration
│   ├── urls.py                Auth endpoints (login, profile)
│   ├── forms.py               User registration form
│   ├── admin.py               User admin configuration
│   ├── templates/             Auth templates
│   └── migrations/            User schema changes
├── db.sqlite3                 SQLite database
├── manage.py                  Django CLI entry point
└── idea.txt                   Project requirements & design notes

```

### How it fits together

**Request flow:**

1. User authenticates via `/login` (users app) and gets assigned a role (fan, coach, official)
2. Dashboard routes to appropriate views based on role:
   - **Fans** → view league table (`/league/`), check matchday results (`/league/matchday/<md>/`)
   - **Coaches** → manage their team (`/league/manage_team/`), set lineups (`/league/matches/<id>/manage_lineup/`)
   - **Officials** → create/edit matches (`/league/matches/`), simulate tournament (`/league/simulate/`)
3. When a match is played/updated, team statistics are atomically updated via `_update_team_stats()` helper
4. League table is sorted by points (won×3 + drawn), then goal difference, then goals scored
5. Starting eleven and substitutes are tracked per match for display to fans

**Data model:**
- `CustomUser` extends Django's `AbstractUser` with role & team FK
- `Team` tracks wins/draws/losses/goals and computes points/goal_difference dynamically
- `Match` links home/away teams, stores scores, matchday number, and played status
- `Player` belongs to a team, has position/role info
- `StartingEleven` & `Substitutes` many-to-many through models linking players to matches

## How to run it

### Prerequisites
- Python 3.8+
- pip

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Thorium234/kibaii_django-tournament-runner.git
cd kibaii_django-tournament-runner

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django==5.2.7

# Apply migrations
python manage.py migrate

# Create a superuser (admin account)
python manage.py createsuperuser

# Seed 20 teams
python manage.py seed_teams

# Run development server
python manage.py runserver
```

### Running the server
```bash
python manage.py runserver
# Server runs at http://localhost:8000/
```

### Admin panel
```
http://localhost:8000/admin/
```
Log in with superuser credentials to manage users, teams, matches, and players directly.

### Available management commands

```bash
# Seed initial 20 teams into the database
python manage.py seed_teams

# Generate & simulate 380 matches across 38 matchdays, then save match results
python manage.py simulate_tournament
```

### First-time workflow
1. **Create superuser** → Log in to `/admin/`
2. **Seed teams** → `python manage.py seed_teams`
3. **Create users** → Add fan/coach/official accounts in admin, assign teams to coaches
4. **Simulate tournament** (optional) → `python manage.py simulate_tournament` or manually add matches
5. **Visit** → `/league/` to view league table

## Key Features

### For Officials
- Create, edit, and delete matches
- Set match results (home win, away win, draw, not played)
- Automatic team statistics updates on match creation/update/delete
- View all matches and manage fixtures

### For Coaches
- Manage their assigned team's player roster
- Add, edit, and delete players with positions and roles
- Set starting eleven and substitutes for upcoming matches

### For Fans
- View live league table sorted by points, goal difference, goals for
- Check matchday-specific results and fixtures
- See player lineups (starting eleven + substitutes) for each match

### Administration
- Role-based access control (fan, coach, official)
- Django admin interface for direct data management
- Seeding tools for quick tournament setup
- Atomic transactions on match updates to prevent data corruption

## Project Status

**Current State:**  
- Core tournament simulation and league management implemented
- Role-based views and CRUD operations working
- Models and database schema set up with SQLite

**In Development / To-Do:**
- Frontend UI/styling (basic HTML templates present but minimal CSS)
- Starting eleven animation/visualization
- Player transfer system between teams
- Match venue management (partially started)
- Configurable point system (currently: win=3pts, draw=1pt, loss=0)
- Comprehensive test suite (tests.py files exist but are minimal)
- API endpoints for third-party integrations


---

For questions or issues, open an issue on the [GitHub repository](https://github.com/Thorium234/kibaii_django-tournament-runner).
