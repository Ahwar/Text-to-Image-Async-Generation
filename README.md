# text_to_image SD_1_4 app
Working example for serving a ML model using FastAPI and Celery.

## Installing dependencies
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Running broker and Backend (to check status -> sudo docker ps)
### Instead of installing rabbitmq and redis, can run a docker container which includes them (no need to install everytime)
### Offical docker containers from rabbitmq and redis to start their servers

**start rabbitmq (broker)**  
`docker run -d -p 5672:5672 rabbitmq`  

**start redis (backend)**    
`docker run -d -p 6379:6379 redis`

**Set environment variables:**
* MODEL_PATH: Hugging face machine learning model (Online of Offline)

```bash
export MODEL_PATH="/dev/stable-diffusion-v1-4/"
```
this model path is for the model downloaded in below section, if you want to use model from huggingface github replace it with `CompVis/stable-diffusion-v1-4`
## Optional: Downlaod model  
Note: If you don't want to use the token, you can also simply download the model weights (after having accepted the license) and pass the path to the local folder to the StableDiffusionPipeline.

```bash
git lfs install
git clone https://huggingface.co/CompVis/stable-diffusion-v1-4
```

Assuming the folder is stored locally under `./stable-diffusion-v1-4` change local path 
with the path above


## starting required services

**start celery server**

```
celery -A celery_task_app.worker worker -l info --concurrency 1
```  

(Optional) To automaticaly reload celery after making changes in celery use this command instead of above (previosuly make changes, need to manually to restart celery service)
```
watchmedo auto-restart --directory=celery_task_app/ --pattern=*.py --recursive -- celery -A celery_task_app.worker worker -l info --concurrency 1
```


**start uvicorn api server**  
run in new terminal  
```
uvicorn --reload app:app
```
**start streamlit server**  
in new terminal  
```
streamlit run main.py
```
