import os
import requests
import json

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
    # Use only Grok API (OpenAI fallback disabled)
    print("🤖 Using Grok API only...")
    return gpt_request_grok(text)

def gpt_request_grok(text):
    # Get Grok API key from environment
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        return "❌ Grok API key not configured. Please set GROK_API_KEY environment variable."

    try:
        # Grok API endpoint
        url = "https://api.x.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Prepare the full prompt
        full_prompt = prep_reqs + " \n " + text

        data = {
            "model": "grok-3",  # Updated to grok-3 as per API error message
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        # Make API request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for bad status codes

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        print(f"Input: {text}")
        formatted_content = content.replace("Example", "\nEx.")
        print(f"Response: {formatted_content}")

        return formatted_content

    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Grok API Error: {str(e)}"
        if hasattr(e.response, 'status_code'):
            error_msg += f" (Status: {e.response.status_code})"
            if hasattr(e.response, 'text'):
                error_msg += f" - Response: {e.response.text[:200]}"
        print(error_msg)
        return error_msg
    except KeyError as e:
        error_msg = f"❌ Grok API Response Error: Invalid response format - {str(e)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Grok API Unexpected Error: {str(e)}"
        print(error_msg)
        return error_msg

# Test function (uncomment to test)
# answer = gpt_request("on the other hand")
# print(answer)
