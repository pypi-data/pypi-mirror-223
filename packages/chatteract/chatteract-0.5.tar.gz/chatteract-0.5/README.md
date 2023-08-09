# ChatterAct

ChatterAct is a Python package developed to streamline the integration of OpenAI's GPT-4 function calling capabilities into your applications. Its primary goal is to provide a simplified, yet flexible mechanism for exposing numerous functions to the AI model with minimal effort. ChatterAct handles the execution and piping, enabling you to start simple with one or two AI functions and expand as the complexity of your project grows.

Basically, what you need to do to get started is to follow a simple pattern for the functions that you want to expose to GPT, and to use the wrapper for the GPT calling.

## Installation

Use pip to install it and then try one of the examples described below:

```
pip install chatteract
```

## Background

With the function calling capability of the models `gpt-4-0613` and `gpt-3.5-turbo-0613` it is simple to make it easy to integrate GPT into your own applications. With it, you can expose the AI to your own functions without having to ask it to provide the output in the form of json (as this is done automatically).

When implementing some initial functions, my own first project's integration to the API got a bit unmanagable. At the same time I wanted to keep my integrations lightweight and not dependent on large automation frameworks for LLM's. Given this I created this lightweight solution that makes it easy to create new functions that GPT can call to talk directly to my applications.

It was also obvious that the API's for this new functionality was a bit unstable, as I could see that I got responses that included invalid json and also frequent 500 responses from the API.

In my small package, I have built in functionality for this.

- An easy way to expose your own functions to GPT
- A simple pattern that makes it easy to extend the number of functions in a good way.
- Handling of responses that aren't valid
- Handling of 500 responses from the API.
- Handling of token counting in API requests.

In short, chatter-act is a package that makes it easy to get started with GPT function calling, and grow the number of exposed functions without seeing the project become unmanageble.

## Key Functions

ChatterAct primarily exposes two significant functions:

1. `get_ai_function`: This function helps create an AI function object with a specific function, its argument handler, and a function description.

2. `handle_openai_response_and_execute_functions`: This function processes responses from the OpenAI API and manages the execution of the appropriate AI functions.

## A Basic Example

Let's consider a simple example using ChatterAct to expose a `hello_world` function to OpenAI:

```python
from chatteract import handle_openai_response_and_execute_functions, get_ai_function
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# This is the function to be executed
def hello_world(name):
    return f"Hello, {name}!"

# This is the description of the function
hello_world_description = {
    'name': 'hello_world',
    'description': 'A function to greet a user.',
    'parameters': {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
                'description': 'The name of the user.'
            }
        }
    }
}

# This is the function argument handler
def hello_world_arg_process(arguments):
    name = arguments.get('name')
    return (name,)

# Create the AI function
hello_world_ai_function = get_ai_function('hello_world', hello_world, hello_world_arg_process, hello_world_description)

# OpenAI settings
openai_settings = {
    "model": "gpt-4-0613",
    "url": "https://api.openai.com/v1/chat/completions",
    "max_retries": 3,
    "retry_delay": 3,
    "max_consecutive_function_calls": 1,
    "max_tokens": 8000,
    "headers": {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    }
}


# Start the conversation with a system message
messages = [
    {
        'role': 'system',
        'content': 'This is a system message to start the conversation.'
    },
    {
        'role': 'user',
        'content': 'Can you greet Alice for me?'
    }
]

def main():
    response = handle_openai_response_and_execute_functions(messages, [hello_world_ai_function], openai_settings)
    print(response[-1]['content'])

if __name__ == "__main__":
    main()
```

In this example, `hello_world` is a function that greets a user. It is combined with its description and argument handler using `get_ai_function` to create an AI function. This AI function is then used in `handle_openai_response_and_execute_functions` to process and handle OpenAI's responses.

Adding another function follows a similar process. Just create another AI function and include it in the list of functions passed to `handle_openai_response_and_execute_functions`. This makes it easy to expose multiple functions to the AI.

## AI Function Structure

Each AI function in ChatterAct has three main components:

1. The function: The actual Python function that gets executed.

2. The function argument handler: Processes the arguments that the function requires.

3. The function description: Contains metadata about the function, including its name, description, and the parameters it accepts.

## The get_ai_function

The `get_ai_function` is used to generate an AI function object. This function takes the following parameters:

- `unique_identifier`: A unique identifier for the function.
- `function`: The actual function that should be executed.
- `function_arg_handler`: A handler function that processes the arguments for the `function`.
- `description`: The description of the function.

Here's an example of how to use it:

```python
from chatteract import get_ai_function

# This is the function to be executed
def hello_world(name):
    return f"Hello, {name}!"

# This is the function argument handler
def hello_world_arg_process(arguments):
    name = arguments.get('name')
    return (name,)

# This is the description of the function
hello_world_description = {
    'name': 'hello_world',
    'description': 'A function to greet a user.',
    'parameters': {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
                'description': 'The name of the user.'
            }
        }
    }
}

# Create the AI function
hello_world_ai_function = get_ai_function('hello_world', hello_world, hello_world_arg_process, hello_world_description)
```

This code block creates an AI function `hello_world`, which can be used in `handle_openai_response_and_execute_functions` to process and handle OpenAI's responses.

## OpenAI Settings

Here is an example openai settings that works.

```
openai_settings = {
    "model": "gpt-4-0613",
    "url": "https://api.openai.com/v1/chat/completions",
    "max_retries": 3,
    "retry_delay": 3,
    "max_consecutive_function_calls": 1,
    "max_tokens": 8000,
    "headers": {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    }
}
```

`max_retries` is the number of times the script tries to call the API when the response contains badly formatted json in the arguments.
`retry_delay` is the number of seconds that the AI should wait if an error occurs before trying again.
`max_consecutive_function_calls` is used to make sure that the AI doesn't end up in a strange loop. This sometimes happens, and the AI sort of start giving itself content together with the function call, and leads to the AI making a new function call based on its own instructions.

# Collaboration

if you want to help out, feel free to raise tickets or create your own pull requests. I am also planning to add some handy out of the box functions.
