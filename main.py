from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()

# fakeDatabase = {
#     1: {'task': 'Clean car'},
#     2: {'task': 'Write blog'},
#     3: {'task': 'Start stream'},
# }


@app.get("/")
def get_items(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/{id}")
def get_item(idd: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(idd)
    return item


# # option 1 formatting as str
# @app.post("/")
# def add_item(item: str):
#     new_id = len(fakeDatabase.keys()) + 1
#     fakeDatabase[new_id] = {"task": item}
#     return fakeDatabase


# option 2 creating pydantic class
@app.post("/")
def add_item(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# # option 3 requesting body
# @app.post("/")
# def add_item(body: Body()):
#     new_id = len(fakeDatabase.keys()) + 1
#     fakeDatabase[new_id] = {"task": body["task"]}
#     return fakeDatabase


@app.put("/{id}")
def update_item(idd: int, item: schemas.Item, session: Session = Depends(get_session)):
    item_obj = session.query(models.Item).get(idd)
    item_obj.task = item.task
    session.commit()
    return item_obj


@app.delete("/{id}")
def update_item(idd: int, session: Session = Depends(get_session)):
    item_obj = session.query(models.Item).get(idd)
    session.delete(item_obj)
    session.commit()
    session.close()
    return "Item was deleted"
