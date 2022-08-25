from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from todo_project.tasks.models import Tasks, SubTask
from todo_project.users.language import convert_data_into_json
from todo_project.users.models import User

class TodoCRUD:
    def __init__(self, request_data, ):
        """
        Form this method set the schema request data.
        :param request_data: schema request data
        """
        self.request_data = request_data

    @classmethod
    async def create_task(cls, task, authorize: AuthJWT = Depends()):
        req_data = convert_data_into_json(task)
        current_user_name = authorize.get_jwt_subject()
        current_user = await User.check_is_username_exists(current_user_name)
        try:
            return await Tasks.create_task(req_data, current_user)
        except:
            return None


    @classmethod
    async def show_task(cls, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        try:
            return await Tasks.find_tasks(current_user_name)
        except:
            return None

    @classmethod
    async def update_todo_task(cls, task_id, task_update, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        try:
            if not (await Tasks.find_task(task_id, current_user_name)):
                return {'data':'You unable to update this tasks because your are not owner of this tasks.'}
            else:
                return await Tasks.update_task(task_id, task_update)
        except:
            return None


    @classmethod
    async def get_task(cls, task_id, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        try:
            if not (await Tasks.find_task(task_id, current_user_name)):
                return {'data': 'You unable to See this tasks because your are not owner of this tasks.'}
            return await Tasks.find_task(task_id, current_user_name)
        except:
            return None

    @classmethod
    async def delete_user_task(cls, task_id, authorize):
        current_user_name = authorize.get_jwt_subject()
        try:
            if not (await Tasks.find_task(task_id, current_user_name)):
                return {'data': 'You unable to delete this tasks because your are not owner of this tasks.'}
            else:
                return await Tasks.delete_task(task_id)
        except:
            return None


class SubTaskCRUD:

    def __init__(self, request_data, ):
        """
        Form this method set the schema request data.
        :param request_data: schema request data
        """
        self.request_data = request_data

    @classmethod
    async def create_subtask(cls, subtask, task_id, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        req_data = convert_data_into_json(subtask)
        try:
            if not (await Tasks.find_task(task_id, current_user_name)):
                return {'data': 'You unable to add SubTasks in this task because your are not owner of this tasks.'}
            else:
                return await SubTask.create_subtask(req_data, task_id)
        except Exception as e:
            print(e)
            return {'Error': 'At Service layer'}

    @classmethod
    async def show_subtask(cls, task_id, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        try:
            if not (await Tasks.find_task(task_id, current_user_name)):
                return {'data': 'You unable to see SubTasks of this task because your are not owner of this tasks.'}
            else:
                return await SubTask.find_subtasks(task_id)
        except Exception as e:
                return {'Error': 'At Service layer'}

    @classmethod
    async def update_todo_subtask(cls, subtask_id, task_update, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        try:
            if not (await SubTask.find_owner_from_subtask(subtask_id, current_user_name)):
                return {'data': 'You unable to update this subtasks because your are not owner of this tasks.'}
            else:
                return await SubTask.update_subtask(subtask_id, task_update)
        except:
            return None

    @classmethod
    async def get_specific_subtask(cls, subtask_id, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        try:
            if not (await SubTask.find_owner_from_subtask(subtask_id, current_user_name)):
                return {'data':'You unable to see the subtask because you are not owner'}
            else:
                return await SubTask.find_subtask_using_todo_id(subtask_id)
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def delete_specific_subtask(cls, subtask_id, authorize: AuthJWT = Depends()):
        current_user_name = authorize.get_jwt_subject()
        try:
            if not (await SubTask.find_owner_from_subtask(subtask_id, current_user_name)):
                return {'data': 'You unable to delete the subtask because you are not owner'}
            else:
                return await SubTask.delete_subtask(subtask_id)
        except Exception as e:
            print(e)
            return None