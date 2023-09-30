from fastapi import FastAPI,UploadFile,Form,Response
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items(
	        id INTEGER PRIMARY KEY,
	        title TEXT NOT NULL,
	        image BLOB,
	        price INTEGER NOT NULL,
	        description TEXT,
	        place TEXT NOT NULL,
	        insertAT INTEGER NOT NULL
);
            """)

app = FastAPI()

# 글쓰기 페이지에서 업로드
@app.post('/items')
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):

    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title, image, price, description, place, insertAt)
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})
                """)
    con.commit()
    return '200'

# 메인 페이지에서 정보읽기
@app.get('/items')
async def get_items():
    # 컬럼명도 같이 가져옴
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items
                       """).fetchall()
    return JSONResponse(
        jsonable_encoder(
        dict(row) for row in rows
        )
        )
    

# 이미지 가져오기
@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id = {item_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes))


# 채팅
class Memo(BaseModel):
    id:int
    content:str
    
memos = []    

@app.post("/memos")
def create_memo(memo:Memo):
    memos.append(memo)
    return "메모 추가에 성공했습니다!"

@app.get("/memos")
def read_memo():
    return memos

@app.put("/memos/{memo_id}")
def put_memo(req_memo:Memo):
    for memo in memos:
        if memo.id==req_memo.id:
            memo.content=req_memo.content
            return'성공했습니다!'
    return '그런 메모는 없습니다!'
        
@app.delete("/memos/{memo_id}")   
def delete_memo(memo_id):
    for index,memo in enumerate(memos):
        if memo.id==memo_id:
            memos.pop(index)
            return'성공했습니다!'
    return '그런 메모는 없습니다!'

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

