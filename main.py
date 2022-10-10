import streamlit as st
import torch

import requests
from time import sleep, time

import json
from PIL import Image
import numpy as np


def get_results(poll_interval=1, max_attempts=45):

    predict_result_uri = base_uri + "/churn/result/" + task_id
    attempts = 0
    result = None
    while attempts < max_attempts:
        attempts += 1
        result_response = requests.get(predict_result_uri)
        print(attempts, "======response code", result_response.status_code, sep=" | ")
        if result_response.status_code == 200:
            result = result_response.json()["probability"]
            break
        sleep(poll_interval)
    return result

# take user input from streamlit
user_input = st.text_input("enter text to generate image")
post_data = {"user_input": str(user_input)}
# generate 2 imagesk, duplicate text
# prompt = [str(user_input)] * 1

# when input is entered
if user_input:
    # st.text("generating image from text:\t" + prompt[0])
    base_uri = r"http://127.0.0.1:8000"
    predict_task_uri = base_uri + "/churn/predict"
    # message that model is loading
    st.text("Sending the request")
    task = requests.post(predict_task_uri, json=post_data)
    task_id = task.json()["task_id"]
    st.text("prediction request sent with request_id: " + task_id)

    st.text("getting prediction result")
    prediction = get_results(2, 35)
    if prediction != None:
        image = Image.fromarray(np.array(json.loads(prediction), dtype="uint8"))

        # save the image
        # image.save(str(time()) + user_input + ".png")

        # show image
        st.image(image)
    else:
        st.text("an error occured, please send request again")
