from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/users')
async def all_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def post_user(username, age) -> User:
    if len(users) == 0:
        user_id = 0
    user_id = len(users) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return users[user_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/users/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id - 1)
        return f'User {user_id} has been deleted.'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
