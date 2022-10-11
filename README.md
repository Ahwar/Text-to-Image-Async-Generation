# ServingMLFastCelery
Working example for serving a ML model using FastAPI and Celery.


**Set environment variables:**
* MODEL_PATH: Hugging face machine learning model (Online of Offline)

```bash
export MODEL_PATH="/dev/stable-diffusion-v1-4/"
```

## Installing dependencies
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Running broker and Backend
**start rabbitmq (broker)**
`docker run -d -p 5672:5672 rabbitmq`  

**start redis (backend)**  
`docker run -d -p 6379:6379 redis`


## starting required services
**start uvicorn api server**  

```
uvicorn --reload app:app
```

**start celery server**

```
celery -A celery_task_app.worker worker -l info
```  

**start streamlit server**  

```
streamlit run main.py
```
