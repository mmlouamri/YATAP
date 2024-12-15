import uuid
from fastapi import APIRouter, HTTPException, Response, status
from app.core.auth.dependencies import UserDep
from app.features.todos.models import TodoDB
from app.features.todos.schemas import TodoSchema, TodoCreateSchema, TodoUpdateSchema, TodosSchema

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=TodosSchema)
async def index(user: UserDep, offset: int = 0, limit: int = 10):
    todos = (
        await TodoDB.filter(owner=user)
        .order_by("created_at")
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {"data": todos, "count": len(todos)}


@router.get("/{todo_id}", response_model=TodoSchema)
async def show(todo_id: uuid.UUID, user: UserDep):
    todo = await TodoDB.filter(id=todo_id, owner=user).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("/", response_model=TodoSchema)
async def store(todo: TodoCreateSchema, user: UserDep):
    created_todo = await TodoDB.create(**todo.model_dump(), owner=user)
    return created_todo


@router.put("/{todo_id}", response_model=TodoSchema)
async def update(todo_id: uuid.UUID, todo: TodoUpdateSchema, user: UserDep):
    to_update_todo = await TodoDB.filter(id=todo_id, owner=user).first()
    if not to_update_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    updated_todo = await to_update_todo.update_from_dict(todo.model_dump(exclude_unset=True))
    await updated_todo.save()
    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(todo_id: uuid.UUID, user: UserDep):
    todo = await TodoDB.filter(id=todo_id, owner=user).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    await todo.delete()
    return Response(status_code=204)
