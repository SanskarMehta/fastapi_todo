import os

from beanie import init_beanie, Document
import motor.motor_asyncio
from dotenv import load_dotenv, find_dotenv

from todo_project.tasks.models import Tasks, SubTask
from todo_project.users.models import User
from config import DevelopmentConfig


async def init_db():
    # Crete Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(DevelopmentConfig.MONGODB_DATABASE_URL)
    # Init beanie with the Product document class and a database
    await init_beanie(database=client.todoapp, document_models=[Tasks,User,SubTask])
