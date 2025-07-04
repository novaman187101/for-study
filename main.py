from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#get 요청은 url에 데이터를 담아서 보내야함

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
    name: str
    age: int

#post 요청은 body에 데이터를 담아서 보내야함

@app.post("/user")
def create_user(user:User):
    return {
        "message": f"사용자 {user.name}이(가) 생성되었습니다.", 
        "age": user.age
        }


class Student(BaseModel):  #class 선언 필수
    name: str   #각 변수 입력 규칙
    level: int
    cn:int 

@app.post("/Student")
def create_student(student: Student):
    return {
        "message": f"사용자 {student.name}이(가) 생성되었습니다.", 
        "level": student.level,
        "cn": student.cn
        }

#mkdir = 폴더 만들기 명령어
#cd는 그 폴더에 널기