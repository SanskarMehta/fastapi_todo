from uuid import UUID
from fastapi import Depends, status, APIRouter
from fastapi_jwt_auth import AuthJWT
from database import init_db
from todo_project.tasks.schemas import TasksCreate, TasksUpdate
from todo_project.tasks.service import TodoCRUD as todo_service
from todo_project.tasks.service import SubTaskCRUD as subtask_service

todo_router = APIRouter()


@todo_router.on_event("startup")
async def start_db():
    await init_db()


@todo_router.post('/task', status_code=status.HTTP_201_CREATED, tags=['tasks'])
async def create(task: TasksCreate, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await todo_service.create_task(task, authorize)


@todo_router.get('/task', tags=['tasks'])
async def all(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    tasks = await todo_service.show_task(authorize)
    return tasks


@todo_router.get('/task/{task_id}', tags=['tasks'])
async def get_perticular_task(task_id: UUID, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await todo_service.get_task(task_id, authorize)


@todo_router.patch('/task/{task_id}', tags=['tasks'])
async def update_task(task_id: UUID, task_update: TasksUpdate, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await todo_service.update_todo_task(task_id, task_update, authorize)


@todo_router.delete('/task/{task_id}', tags=['tasks'])
async def delete_user_task(task_id: UUID, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await todo_service.delete_user_task(task_id, authorize)


@todo_router.post('/task/{task_id}/subtask', status_code=status.HTTP_201_CREATED, tags=['sub-tasks'])
async def create_subtask(subtask: TasksCreate, task_id: UUID, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await subtask_service.create_subtask(subtask, task_id, authorize)


@todo_router.get('/task/{task_id}/subtask', tags=['sub-tasks'])
async def all_subtask(task_id: UUID, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    tasks = await subtask_service.show_subtask(task_id, authorize)
    return tasks


@todo_router.patch('/task/subtask/{subtask_id}', tags=['sub-tasks'])
async def update_task(subtask_id: UUID, task_update: TasksUpdate, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await subtask_service.update_todo_subtask(subtask_id, task_update, authorize)


@todo_router.get('/task/subtask/{subtask_id}', tags=['sub-tasks'])
async def get_perticular_subtask(subtask_id: UUID, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await subtask_service.get_specific_subtask(subtask_id, authorize)


@todo_router.delete('/task/subtask/{subtask_id}', tags=['sub-tasks'])
async def delete_perticular_subtask(subtask_id: UUID, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await subtask_service.delete_specific_subtask(subtask_id, authorize)