from openai import OpenAI

# client = OpenAI(api_key="5738154551:AAF8Ru5dVHE5bpx0mjEdc6orXFNCyvY4cec")

# client.api_key = "5738154551:AAF8Ru5dVHE5bpx0mjEdc6orXFNCyvY4cec"
import os
import httpx
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
gpt = OpenAI(api_key=api_key)

prep_reqs = ("I will give you a word in English and I will expect you will respond me translation"
             " on russian language. Style of response should be like this (Example should be on a new line) "
             "\"complain  (kəmˈplān) - жаловаться / сетовать. "
             "Example - My brother always complains when he has to do his homework.\" "
             "On the next line give translation of example to russian."
             "If you will get not only one word but complete sentence in English, try to "
             "translate it to Russian and give short definition in Russian language "
             "about meaning that sentence or expression. "
             "If you will get something else which doesn't fit to previous requirements just "
             "answer \"I dont get it, try ask in other words, please\". --")


def gpt_request(text):
    response = gpt.chat.completions.create(
        messages=[{"role": "user",
                   "content": (prep_reqs + " \n " + text)}],
        model="gpt-4o"
    )
    print(text)
    print(response.choices[0].message.content.replace("Example", "\nEx."))
    return response.choices[0].message.content.replace("Example", "\nEx.")

# answer = gpt_request("on the other hand")
# print(answer.choices[0].message.content.replace("Example", "\nEx."))
