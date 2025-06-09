from fastapi import FastAPI
from api.routes import cbt, habits, activity, sleep
from api.routes import moods, recap, journal, schedule
from api.routes import ping, journals

def start_api():
    app = FastAPI(title="Avrana Core API")

    # Internal APIs
    app.include_router(cbt.router)
    app.include_router(habits.router)
    app.include_router(activity.router)
    app.include_router(sleep.router)
    app.include_router(moods.router)
    app.include_router(recap.router)
    app.include_router(journal.router)
    app.include_router(schedule.router)

    # Global routers
    app.include_router(ping.router)
    app.include_router(journals.router)

    return app  # ✅ RETURN — DO NOT run uvicorn here
