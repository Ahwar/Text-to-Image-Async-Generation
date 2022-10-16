from pydantic import BaseModel
# all the objects used in the deployment process
class Client(BaseModel):
    """ Features for image generation """
    prompt: str
    image: str
    mask_image: str


class Task(BaseModel):
    """ Celery task representation """
    task_id: str
    status: str


class Prediction(BaseModel):
    """ Prediction task result """
    task_id: str
    status: str
    result: str
