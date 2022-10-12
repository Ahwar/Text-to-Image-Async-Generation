from fastapi import FastAPI
from fastapi.responses import JSONResponse
from celery.result import AsyncResult #to get result asynchronously
from celery_task_app.tasks import generate_image_single 
from models import Client, Task, Prediction 

# making an object of FastAPI
app = FastAPI()

# post request user using FastAPI
@app.post('/image-generation', response_model=Task, status_code=202)
async def generate_task(client: Client):
    """Create celery image generation task. Return task_id to client in order to retrieve result"""
    task_id = generate_image_single.delay(dict(client))
    return {'task_id': str(task_id), 'status': 'Processing'}

# get request to user using from model to get result
@app.get('/get-result/{task_id}', response_model=Prediction, status_code=200,
         responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}})
async def get_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': 'Success', 'result': str(result)}

