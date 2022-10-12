from pydantic import BaseModel
class Client(BaseModel):
    """ Features for image generation """
    user_input: str
    no_of_images: int


class Task(BaseModel):
    """ Celery task representation """
    task_id: str
    status: str


class Prediction(BaseModel):
    """ Prediction task result """
    task_id: str
    status: str
    result: str
