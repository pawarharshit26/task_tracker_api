from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from apis import models, database

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API!"}

@app.post("/tasks/")
def create_task(title: str, db: Session = Depends(get_db)):
    new_task = models.Task(title=title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.put("/tasks/{task_id}")
def update_task(task_id: int, is_done: bool, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_done = is_done
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}