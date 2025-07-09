from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from supabase import create_client, Client

app = FastAPI()

SUPABASE_URL = "https://ubbqlekazairbmqwcffl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViYnFsZWthemFpcmJtcXdjZmZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjU1NDEsImV4cCI6MjA2NzYwMTU0MX0.S3YQYH2WhfB6LN0YmCLNpoCK7g1IZuCVVAd-q70lrSs"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI 서버 실행 명령어
# uvicorn main:app --reload   

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/hello")
def read_hello():
    print("Hello endpoint was called")
    return {"message": "Hello, FastAPI!"}

# http://127.0.0.1:8000/hello/디디
@app.get("/hello/{name}")
def read_hello_name(name: str):
    print(name)
    return {"message": f"안녕하세요, {name}님!"}

# http://127.0.0.1:8000/greet?name=디디디디디&age=20
@app.get("/greet")
def read_greet(name: str = "방문자", age: int = 0):
    return {"message": f"안녕하세요, {name}님!"}

@app.get("/info")
def read_info(name: str, city: str):
    return {"message": f"{name}님, {city}에 오신 것을 환영합니다!"}


class User(BaseModel):
    # name: str
    # age: int
    name: str = Field(..., min_length=2, max_length=10)
    age: int = Field(..., ge=0, le=120)  # 0 이상 120 이하

user_list = []
user_id_counter = 1

@app.post("/user")
def create_user(user: User):
    global user_id_counter
    new_user = user.dict()
    new_user['id'] = user_id_counter
    user_list.append(new_user)
    user_id_counter += 1
    return {
        "message": f"사용자 {user.name}이(가) 생성되었습니다.",
        "id": new_user['id'],
        "age": user.age
    }

# 사용자 전체 조회 (GET)
@app.get("/users")
def get_users():
    return user_list


# 특정 사용자 조회
@app.get("/user/{user_id}")
def get_user(user_id: int):
    for user in user_list:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

@app.put("/user/{user_id}")
def update_user(user_id: int, updated_user: User):
    for user in user_list:
        if user["id"] == user_id:
            user["name"] = updated_user.name
            user["age"] = updated_user.age
            return {
                "message": f"{user['name']}님의 정보가 업데이트되었습니다.",
                "id": user["id"],
                "age": user["age"]
            }
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

# 특정 사용자 삭제
@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for idx, user in enumerate(user_list):
        if user["id"] == user_id:
            user_list.pop(idx)
            return {"message": f"{user['name']}님이 삭제되었습니다."}
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")


class Student(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    grade: int = Field(..., ge=1, le=3)
    classroom: int = Field(..., ge=1, le=10)

@app.post("/student")
def register_student(student: Student):
    return {
        "message": f"{student.grade}학년 {student.classroom}반 {student.name} 학생이 등록되었습니다."
    }

class Todo(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    done: bool = False

todos: List[dict] = []
todo_id_counter = 1

# 할 일 등록
@app.post("/todos")
def create_todo(todo: Todo):
    print("할 일 등록 요청:", todo)
    result = supabase.table("todos").insert(todo.dict()).execute()
    print("supabse 할 일 등록 요청:", result)

    return result.data[0]

# 전체 할 일 조회
@app.get("/todos")
def get_todos():
    return todos

# 완료된 할 일 조회
@app.get("/todos/complete")
def get_todos_complte(done: bool):
    list = []
    for t in todos:
        if t["done"] == done:
            list.append(t)

    return list

# 특정 할 일 조회
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for t in todos:
        if t["id"] == todo_id:
            return t
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다.")

# 할 일 수정
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    for t in todos:
        if t["id"] == todo_id:
            t["title"] = todo.title
            t["done"] = todo.done
            return {"message": f"{todo_id}번 할 일이 수정되었습니다."}
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다.")

# 할 일 삭제
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for idx, t in enumerate(todos):
        if t["id"] == todo_id:
            todos.pop(idx)
            return {"message": f"{todo_id}번 할 일이 삭제되었습니다."}
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다.")