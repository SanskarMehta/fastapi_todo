from beanie import init_beanie, Document
import motor.motor_asyncio

from todo_project.tasks.models import Tasks, SubTask
from todo_project.users.models import User


async def init_db():
    # Crete Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb+srv://sanskar2420:inx12345@cluster0.b4y5h.mongodb.net/test"
    )
    # Init beanie with the Product document class and a database
    await init_beanie(database=client.todoapp, document_models=[Tasks,User,SubTask])
