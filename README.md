# Real-Time Polling Platform (Backend)
A minimal Django + DRF backend for a real-time polling application (assignment submission).
This project focuses on clarity and core functionality:
- Organizer authentication (register / login) using JWT.
- Create sessions (polls), questions and options.
- Participants join with session join code and submit votes.
- Voting endpoint returns 202 Accepted and counts votes asynchronously using an in-process queue worker (suitable for demo).
- Simple Server-Sent Events (SSE) endpoint to stream live results (polling DB every 1s) for demo purposes.

## Tech stack
- Python, Django 4.2
- Django REST Framework
- MySQL (configuration in `.env`)
- No Redis/Celery in this demo (explain trade-offs in README)

## Setup (quick)
1. Make a Python 3.10+ virtualenv and activate it.
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in project root with:
   ```
   SECRET_KEY=you-should-change-this
   DEBUG=True
   DB_NAME=your_db
   DB_USER=your_user
   DB_PASS=your_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create superuser (organizer):
   ```
   python manage.py createsuperuser
   ```
6. Run server:
   ```
   python manage.py runserver
   ```

## Notes and trade-offs
- **Duplicate-vote prevention**: This demo uses a `participant_id` (UUID) supplied by the client and stored in a cookie. The backend enforces one vote per participant per question. This is robust for casual use but can be circumvented by clearing cookies or changing device. For stronger prevention, use authenticated participant accounts or IP+fingerprint heuristics and rate-limiting.
- **Real-time updates**: Implemented with SSE that polls the database every 1 second. This is easy to demo but inefficient at scale. Production systems should use WebSockets (e.g., Django Channels) with Redis pub/sub or a message broker to push updates.
- **Async vote processing**: A simple in-process `queue.Queue` worker counts votes asynchronously. It's easy to run but not resilient across multiple processes/hosts. For scale use Celery + Redis/RabbitMQ.
- **Containerization**: A sample `docker-compose.yml` is included with MySQL service.

## Files included
- Django project `realtime_poll/`
- Apps: `accounts`, `polls`
- `docker-compose.yml` and `Dockerfile` (simple)
- `api_docs_postman.json` - a basic Postman collection stub

Open the folder in VSCode and you can run the Django server. Good luck!
