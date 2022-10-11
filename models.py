from pydantic import BaseModel
class Customer(BaseModel):
    """ Features for customer prediction """
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
    probability: str
