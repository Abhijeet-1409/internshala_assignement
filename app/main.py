import uvicorn
from app.config.config import settings
from app.db.database import Database
from app.routers import auth, users
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status 
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
   
    try :
        # Intialize all resorces
        app.state.db = Database()

        await app.state.db.init_db()

        yield

    except Exception as exc :
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server is down. Unable to initialize resources."
        )
    finally :
        # Releasing all resouces 
        app.state.db.close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
