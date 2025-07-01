from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.classes.Users_class import Users

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users/create")
async def register_users(request: Request):
    try:
        data = await request.json()
        # r.validate_input_data(data, "register_user")
        user = Users()
        response = user.register_user(data)
        return response 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/users/login")
async def login_users(request: Request):
    try:
        data = await request.json()
        user = Users()
        response = user.login_users(data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))