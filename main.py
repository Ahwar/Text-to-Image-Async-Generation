import streamlit as st

import requests
from time import sleep

import json
from PIL import Image
import numpy as np


def get_results(poll_interval=1, max_attempts=45):

    predict_result_uri = base_uri + "/get-result/" + task_id
    attempts = 0
    result = None
    while attempts < max_attempts:
        attempts += 1
        result_response = requests.get(predict_result_uri)
        print(attempts, "======response code", result_response.status_code, sep=" | ")
        if result_response.status_code == 200:
            result = result_response.json()["result"]
            break
        sleep(poll_interval)
    return result

# take user input from streamlit 
user_input = st.text_input("enter text to generate image")

img_no= st.radio(
    "how many images to generate ?",
    ('3', '6', '9'))
img_no = int(img_no)

post_data = {"user_input": str(user_input), "no_of_images": img_no}

# when input is entered
if st.button("Generate"):
    
    base_uri = r"http://127.0.0.1:8000"
    predict_task_uri = base_uri + "/image-generation"
    # message that model is loading
    st.text("generating image from text:\t" + str(post_data["user_input"]))
    task = requests.post(predict_task_uri, json=post_data)
    task_id = task.json()["task_id"]
    st.text("result request sent with request_id: " + task_id)

    result = get_results(2, 44)

    if result != None:
        result = json.loads(result)
        # CONVERT TO COLUMNS
        col1, col2, col3 = st.columns(3)
        # column one
        with col1:
            st.image(Image.fromarray(np.array(result["0"], dtype="uint8")))
            st.image(Image.fromarray(np.array(result["1"], dtype="uint8")))
            st.image(Image.fromarray(np.array(result["2"], dtype="uint8")))
        if img_no ==6:
            # column two
            with col2:
                st.image(Image.fromarray(np.array(result["3"], dtype="uint8")))
                st.image(Image.fromarray(np.array(result["4"], dtype="uint8")))
                st.image(Image.fromarray(np.array(result["5"], dtype="uint8")))

        if img_no ==9:
            # # # column three
            with col3:
                st.image(Image.fromarray(np.array(result["6"], dtype="uint8")))
                st.image(Image.fromarray(np.array(result["7"], dtype="uint8")))
                st.image(Image.fromarray(np.array(result["8"], dtype="uint8")))

    else:
        st.text("an error occured, please send request again")
