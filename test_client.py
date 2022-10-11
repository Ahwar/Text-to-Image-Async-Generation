# debug script for image generation without streamlit

import requests
from time import sleep

import json
from PIL import Image
import numpy as np

test_body = {"user_input":"superman hitting spiderman"}

def dummy_task(data, poll_interval=1, max_attempts=45):
    base_uri = r'http://127.0.0.1:8000'
    predict_task_uri = base_uri + '/churn/predict'
    # task = requests.post(predict_task_uri, json=data)
    i = 1
    for i in range(0, 3):
        task = requests.post(predict_task_uri, json=data)
    task_id = task.json()['task_id']
    
    print(task_id)
    predict_result_uri = base_uri + '/churn/result/' + task_id
    attempts = 0
    result = None
    while attempts < max_attempts:
        attempts += 1
        result_response = requests.get(predict_result_uri)
        print(attempts, "======response code", result_response.status_code, sep=' | ')
        if result_response.status_code == 200:
            result = result_response.json()['probability'] 
            break
        sleep(poll_interval)
    return result


if __name__ == '__main__':
    prediction = dummy_task(test_body)
    image = Image.fromarray(np.array(json.loads(prediction), dtype='uint8'))
    print(type(prediction))
