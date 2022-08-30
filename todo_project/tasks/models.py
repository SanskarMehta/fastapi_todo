from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Insert, Replace
from pydantic import Field
from todo_project.tasks.schemas import TasksUpdate
from todo_project.users.models import User


class Tasks(Document):
    todo_id: UUID = Field(default_factory=uuid4, unique=True)
    status: bool = False
    title: Indexed(str)
    description: str = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    owner: Link[User]

    @classmethod
    async def create_task(cls, data, current_user: User):
        new_blog = cls(**data, owner=current_user)
        await new_blog.insert()
        return new_blog

    @classmethod
    async def find_tasks(cls, name: str):
        user = await User.get_user(name)
        tasks = await cls.find(cls.owner.user_id == user.user_id, fetch_links=True).to_list()
        return tasks

    @classmethod
    async def find_task(cls, task_id: UUID, current_user_name: str):
        try:
            task = await cls.find(cls.todo_id == task_id, cls.owner.username == current_user_name,
                                  fetch_links=True).to_list()
            return task
        except:
            return None

    @classmethod
    async def find_task_using_todo_id(cls, task_id: UUID):
        try:
            return await cls.find_one(cls.todo_id == task_id)
        except Exception as e:
            print(e)
            return {'Error': 'Unable to find the todo task.'}

    @classmethod
    async def update_task(cls, task_id: UUID, data: TasksUpdate):
        try:
            task = await cls.find_task_using_todo_id(task_id)
            await task.update({"$set": data.dict(exclude_unset=True)})
            await task.save()
            return {"Data": "Task is updated Successfully."}
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def delete_task(cls, task_id: UUID):
        try:
            await cls.find_one(cls.todo_id == task_id).delete()
            return {'Data': 'Task is deleted Successfully'}
        except Exception as e:
            print(e)
            return False

    @before_event([Replace, Insert])
    def update_update_at(self):
        self.updated_at = datetime.now()


class SubTask(Document):
    subtask_id: UUID = Field(default_factory=uuid4, unique=True)
    status: bool = False
    title: Indexed(str)
    description: str = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    task: Link[Tasks]

    @classmethod
    async def create_subtask(cls, data, task_id):
        task = await Tasks.find_task_using_todo_id(task_id)
        new_subtask = cls(**data, task=task)
        await new_subtask.insert()
        return new_subtask

    @classmethod
    async def find_subtasks(cls, task_id: UUID):
        tasks = await cls.find(cls.task.todo_id == task_id, fetch_links=True).to_list()
        return tasks

    @classmethod
    async def find_owner_from_subtask(cls, subtask_id, current_user_name):
        subtasks = await cls.find_subtask_using_todo_id(subtask_id)
        todo_id = subtasks.task.todo_id
        task = await Tasks.find_task(todo_id, current_user_name)
        return task

    @classmethod
    async def find_subtask_using_todo_id(cls, subtask_id):
        subtasks = await cls.find_one(cls.subtask_id == subtask_id, fetch_links=True)
        return subtasks

    @classmethod
    async def update_subtask(cls, subtask_id, data: TasksUpdate):
        try:
            subtask = await cls.find_subtask_using_todo_id(subtask_id)
            await subtask.update({"$set": data.dict(exclude_unset=True)})
            await subtask.save()
            return {"Data": "SubTask is updated Successfully."}
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def delete_subtask(cls, subtask_id):
        try:
            await cls.find_one(cls.subtask_id == subtask_id).delete()
            return {'Data': 'Task is deleted Successfully'}
        except Exception as e:
            print(e)
            return False
