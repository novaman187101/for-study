from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from supabase import create_client, Client

supabaes_URL = "https://ubbqlekazairbmqwcffl.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViYnFsZWthemFpcmJtcXdjZmZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjU1NDEsImV4cCI6MjA2NzYwMTU0MX0.S3YQYH2WhfB6LN0YmCLNpoCK7g1IZuCVVAd-q70lrSs"
supabase: Client = create_client(supabaes_URL, key)

app = FastAPI()

# FastAPT
# uvicorn main:app --reload 

#get 요청은 url에 데이터를 담아서 보내야함

#http://localhost:8000/docs 는 확인 사이트

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/hello")
def read_hello():
    print("Hello endpoint was called")
    return {"message": "Hello, FastAPI!"}

#http://127.0.0.1:8000/hello/panzer
@app.get("/hello/{name}")
def read_hello_name(name: str):
    print(name)
    return {"message": f"안녕하세요, {name}님!"}


@app.get("/greet")
def read_greet(name: str = "방문자"):
    return {"message": f"안녕하세요, {name}님!"}

#http://127.0.0.1:8000/info?mane=총통&city=베를린
@app.get("/info")
def read_info(name: str = "총통", city: str = "베를린"):
    return {"message":f"{name}님, {city}에 오신것을 환영합니다"} #f는 format 함수


#class 객체

class User(BaseModel):
    #name: str
    #ge: int

    name : str = Field(...,min_length=2, max_length=10)  #Field는 변수에 대한 추가 정보를 제공
    age: int = Field(..., title="사용자 나이", description="사용자의 나이를 입력하세요", ge=0, le=120)  #ge는 greater than equal, le는 less than equal
#post 요청은 body에 데이터를 담아서 보내야함

#임시 저장 리스트
user_list = []
user_id_counter = 1


@app.post("/user")
def create_user(user:User):
    global user_id_counter  #전역 변수로 선언
    new_user = user.dict()
    new_user["id"] = user_id_counter  #user 객체에 id 추가
    user_list.append(new_user) #user_list에 new_user 객체를 추가
    user_id_counter += 1  #id 카운터 증가
    return {
        "id" : new_user["id"],  #새로운 사용자 id
        "message": f"사용자 {user.name}이(가) 생성되었습니다.", 
        "age": user.age
        }

#사용자 전체 조회
@app.get("/users")
def read_users():
    return user_list

#특정 사용자 조회
@app.get("/user/{user_id}")
def get_user(user_id: int):
    for user in user_list:
        if user["id"] == user_id:
            return user
    return HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")


@app.put("/user/{user_id}")
def update_user(user_id: int, updated_user: User):
    for user in user_list:
        if user["id"] == user_id:
            user["name"] = updated_user.name
            user["age"] = updated_user.age
            return {
                "message": f"사용자 {user_id}이(가) 업데이트되었습니다.",
                "user": user
            }
    return HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")



#특정 사용자 삭제
@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for idx, user in enumerate(user_list):
        if user["id"] == user_id:
            user_list.pop((idx))
            return {"message": f"사용자 {user_id}이(가) 삭제되었습니다."}
    return HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")















class Student(BaseModel):  #class 선언 필수
    #name: str   #각 변수 입력 규칙
    #level: int
    #cn:int#


    name: str = Field(..., min_length=2, max_length=10) 
    level: int = Field(..., ge=1, le=10) 
    cn: int = Field(..., ge=1, le=10) 
    id: int

student_list = []
student_id_counter = 1  #학생 id 카운터

@app.post("/Student")
def create_student(student: Student):
    global student_id_counter  #전역 변수로 선언
    new_student = student.dict()
    new_student["id"] = student_id_counter
    student_list.append(student)  #student_list에 student 객체를 추가
    student_id_counter += 1  #id 카운터 증가
    return {
        "message": f"사용자 {student.name}이(가) 생성되었습니다.", 
        "level": student.level,
        "cn": student.cnS
        }


@app.get("/students")
def read_students():
    return student_list

#특정 사용자 조회
@app.get("/student/{student_id}")
def get_student(student_id: int):
    for student in student_list:
        if student["name"] == student_id:
            return student
    return HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

#특정 사용자 삭제
@app.delete("student/{student_id}")
def delete_student(student_id: int):
    for idx, student in enumerate(student_list):
        if student["name"] == student_id:
            student_list.pop((idx))
            return {"message": f"사용자 {student_id}이(가) 삭제되었습니다."}
    return HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

#mkdir = 폴더 만들기 명령어
#cd는 그 폴더에 널기



todo_list = []
todo_id_counter = 1


class Todo(BaseModel):
    title: str  = Field(..., min_length=1, max_length=50)
    done: bool = False 

todos: List[dict] = []  #할일 목록

@app.post("/todos")
def create_todo(todo: Todo):
   print("할 일 생성 요청:", todo)
   result = supabase.table("todos").insert(todo.dict()).execute()
   return result.data[0]

# 전체 할 일 조회
@app.get("/todos")
def get_todos():
    return todos

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
