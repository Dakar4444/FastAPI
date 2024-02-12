from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Union


app = FastAPI()

task_i = []


class Task(BaseModel):
    """
    Базовая модель задачи
    """

    id_: int
    title: str
    description: str
    status: str


@app.get("/tasks/", response_class=JSONResponse)
async def get_all_tasks():
    """
    Функция вывода
    всех задач
    """
    return JSONResponse(content=str([vars(task) for task in task_i]), status_code=200)


@app.get("/tasks/{task_id}", response_class=Union[JSONResponse])
async def get_one_task(task_id: int):
    """
    Вывод одной задачи по ID
    """
    for task in task_i:
        if task.id_ == task_id:
            return JSONResponse(content=vars(task), status_code=200)

    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/task/new_task/")
async def add_new_task(task: Task):
    """
    Функция добавления новой задачи
    """
    task_i.append(task)
    return {"Добавлена задача": task}


@app.put("/tasks/update/{task_id}")
async def update_task(task_id: int, update_task: Task):
    """
    Функция обновления задачи
    """
    try:
        for task in task_i:
            if task.id_ == task_id:
                task.title = update_task.title
                task.description = update_task.description
                task.status = update_task.status
                return {
                    "обновлено": task,
                    "новое значение": update_task,
                }
    except HTTPException:
        return {"Не найдено": task_id}
    

@app.delete("/tasks/delete/{task_id}")
async def delete_task(del_task_id: int):
    """
    Функция удаления задачи
    """
    try:
        for task in task_i:
            if task.id_ == del_task_id:
                task_i.remove(task)
                return {"Удалено": f"{task}"}

    except HTTPException:
        return {"Задача не найдена": del_task_id}