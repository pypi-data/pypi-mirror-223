from setuptools import setup, find_packages

setup(
    name='chatteract',  # The name of your package
    version='0.2',  # The current version of your package
    packages=find_packages(),  # List of all python packages to include. find_packages() automatically detects all packages and subpackages.
    author='Mattias Aspelund',  # Your name    
    description='A package to handle OpenAI responses and execute function calls.',  # A brief description of your package
    long_description="""ChatterAct is a Python package developed to streamline the integration of OpenAI\'s GPT-4 function calling capabilities into your applications. Its primary goal is to provide a simplified, yet flexible mechanism for exposing numerous functions to the AI model with minimal effort. ChatterAct handles the execution and piping, enabling you to start simple with one or two AI functions and expand as the complexity of your project grows.

Basically, what you need to do to get started is to follow a simple pattern for the functions that you want to expose to GPT, and to use the wrapper for the GPT calling.""",
    url='https://github.com/aspelund/chatter-act',  # Link to the github repo or website
    classifiers=[  # Classifiers help users find your project by categorizing it.
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'tiktoken',
        # add any additional packages that your software needs
    ],  # List of dependencies that Python will automatically install alongside your package
    python_requires='>=3.6',  # Minimum version of Python your package requires
)
