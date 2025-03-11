from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from router.register.register import register_router 
from router.user.users import auth_router
from router.chat_service.chat import chat_router

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Custom-Header"],
)

app.include_router(register_router)
app.include_router(auth_router)
app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True)