import streamlit as st

import requests
from time import sleep

import json
from PIL import Image
import numpy as np

from io import BytesIO


def download_as_json(url):
    response = requests.get(url)
    if response.status_code != 404:
        img = (
            Image.open(BytesIO(response.content))
            .convert("RGB")
            .resize((512, 512), Image.ADAPTIVE)
        )
        return json.dumps(np.array(img).tolist())
    else:
        return None


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
prompt = st.text_input("enter text prompt to generate image")
# take user input from streamlit
image_url = st.text_input("enter input image URL")



# when input is entered
if st.button("Generate"):
    # download image and convert to json
    init_image = download_as_json(image_url)
    post_data = {
        "prompt": str(prompt),
        "image": init_image,
    }

    if init_image == None:
        st.text("The URL you provide does not have any image, Please check URL")
    else:
        # streamlit deafult uri
        base_uri = r"http://127.0.0.1:8000"
        # routes to image generation path
        predict_task_uri = base_uri + "/image-generation"
        # message that model is loading
        st.text("generating image from text:\t" + str(post_data["prompt"]))

        # print("generating image from text:\t" + str(post_data["image"]))
        # getting taskid and displaying
        task = requests.post(predict_task_uri, json=post_data)
        st.text("Your input sample image")
        st.image(
            Image.fromarray(np.array(json.loads(post_data["image"]), dtype="uint8"))
        )
        task_id = task.json()["task_id"]
        st.text("result request sent with request_id: " + task_id)
        st.text("Your image is being generated")

        # polling function to get results (2 seconds between every requests -
        # to get the results, 44 - how many times to ask for results)
        result = get_results(2, 44)

        if result != None:
            # result = json.loads(result)
            st.image(Image.fromarray(np.array(json.loads(result), dtype="uint8")))

        else:
            st.text("an error occured, please send request again")
