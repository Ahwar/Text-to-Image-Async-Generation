import streamlit as st

import requests
from time import sleep

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
post_data = {"user_input": str(user_input), "no_of_images": 9}

# when input is entered
if user_input:
    
    base_uri = r"http://127.0.0.1:8000"
    predict_task_uri = base_uri + "/churn/predict"
    # message that model is loading
    st.text("generating image from text:\t" + str(post_data["user_input"]))
    task = requests.post(predict_task_uri, json=post_data)
    task_id = task.json()["task_id"]
    st.text("prediction request sent with request_id: " + task_id)

    prediction = get_results(2, 35)

    if prediction != None:
        prediction = json.loads(prediction)
        # CONVERT TO COLUMNS
        col1, col2, col3 = st.columns(3)
        # column one
        with col1:
            st.image(Image.fromarray(np.array(prediction["0"], dtype="uint8")))
            st.image(Image.fromarray(np.array(prediction["1"], dtype="uint8")))
            st.image(Image.fromarray(np.array(prediction["2"], dtype="uint8")))

        # column two
        with col2:
            st.image(Image.fromarray(np.array(prediction["3"], dtype="uint8")))
            st.image(Image.fromarray(np.array(prediction["4"], dtype="uint8")))
            st.image(Image.fromarray(np.array(prediction["5"], dtype="uint8")))

        # # column three
        with col3:
            st.image(Image.fromarray(np.array(prediction["6"], dtype="uint8")))
            st.image(Image.fromarray(np.array(prediction["7"], dtype="uint8")))
            st.image(Image.fromarray(np.array(prediction["8"], dtype="uint8")))

    else:
        st.text("an error occured, please send request again")
