import requests
import os
import time
import json
import tiktoken


def get_token_compliant_messages(original_messages, max_tokens):
    encoding = tiktoken.get_encoding("cl100k_base")

    # Start with only the system message
    messages = [original_messages[0]]
    tokens = encoding.encode(messages[0]["content"])

    # Add the messages in reverse order
    for message in reversed(original_messages[1:]):
        msg_content = message["content"]
        temp_tokens = tokens + encoding.encode(msg_content)

        # If the new message fits within the token limit, add it
        if len(temp_tokens) <= max_tokens:
            tokens = temp_tokens
            # Add the new message after the system message
            messages.insert(1, message)
        else:
            break  # Stop adding messages once we hit the token limit

    # Check if we were able to include any user message
    if len(tokens) == len(encoding.encode(messages[0]["content"])):
        raise ValueError(
            "None of the user messages fit within the token limit.")

    return messages, len(tokens)


def send_api_request(messages, api_settings, descriptions):
    required_keys = {"model", "url"}
    if not required_keys.issubset(api_settings.keys()):
        missing_keys = required_keys.difference(api_settings.keys())
        raise KeyError(
            f"Missing required keys in 'api_settings': {', '.join(missing_keys)}")

    headers = api_settings.get("headers", {})
    headers.update({"Content-Type": "application/json"})

    max_tokens = api_settings.get("max_tokens", 4000)
    max_retries = api_settings.get("max_retries", 3)
    retry_delay = api_settings.get("retry_delay", 3)

    messages, token_count = get_token_compliant_messages(messages, max_tokens)

    data = {
        "model": api_settings["model"],
        "messages": messages,
        "functions": descriptions
    }

    response = None
    for i in range(max_retries):
        response = requests.post(
            api_settings["url"], headers=headers, json=data, stream=True)
        if response.status_code != 500:
            break
        time.sleep(retry_delay * (i + 1))

    # Check for errors
    if response.status_code != 200:
        raise Exception(
            f"Request failed with status code {response.status_code}. Headers: {response.headers}\nContent: {response.text}"
        )

    response_json = response.json()

    if 'choices' in response_json and len(response_json['choices']) > 0:
        if 'message' in response_json['choices'][0]:
            return response_json['choices'][0]['message']
        else:
            raise ValueError(
                'Response does not contain "message" in "choices"')
    else:
        raise ValueError(
            'Response does not contain "choices" or "choices" is empty')
