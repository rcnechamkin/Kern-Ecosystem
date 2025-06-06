from fastapi import FastAPI
from api.routes import ping
from api.routes import moods
from api.routes import cbt, habits, activity, sleep
from api.routes import moods, recap, journal, schedule
import uvicorn

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

    # Include routes
    app.include_router(ping.router)

    # Run locally (for development)
    uvicorn.run(app, host="127.0.0.1", port=8000)

