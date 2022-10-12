import importlib
import logging
from celery import Task

from .worker import app

# our worker has 2 tasks
# 1) Load model and 2) Inference of model

class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.

    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logging.info('Loading Model...')
            module_import = importlib.import_module(self.path[0])
            model_obj = getattr(module_import, self.path[1])
            self.model = model_obj()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@app.task(ignore_result=False,
          
          bind=True,
          base=PredictTask,
          path=('celery_task_app.ml.model', 'GenerationModel'),
          name='{}.{}'.format(__name__, 'Churn'))
def generate_image_single(self, data):
    """
    Essentially the run method of PredictTask
    """
    
    return self.model.predict([data])
