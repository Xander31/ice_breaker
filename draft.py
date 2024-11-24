"""
pipenv install python-dotenv
pipenv install langchain-community
pipenv install langchain-openai
pipenv install langchainhub
"""

import os
from dotenv import load_dotenv, dotenv_values


load_dotenv()

print(os.getenv("MY_SECRET_KEY"))

config = dotenv_values(".env")

print(config["EMAIL"])