"""Meeseeks AI chatbot"""
import os
import sys
import openai
from dotenv import load_dotenv


# System message prompt for OpenAI chatbot
SYSTEM_MESSAGE_PROMPT = "You are a friendly AI assistant called Meeseeks. Always introduce yourself to the user. Your job is to help users with their queries."

def construct_message_with_history(user_prompt, history=[]):
    """Construct a message for the chatbot"""
    messages = []

    # add system message prompt
    messages.append({'role':'system', 'content': SYSTEM_MESSAGE_PROMPT})
    # add history
    for msg in history:
        messages.append(msg)    
    # add user prompt
    messages.append({'role':'user', 'content': user_prompt})

    return messages

def get_chat_completion(messages, engine="gpt-35-turbo", model="gpt-35-turbo", temperature=0):
    response = openai.ChatCompletion.create(engine=engine, model=model, messages=messages, temperature=temperature)
    return response.choices[0].message.content

def main(args=None):
    """"Process command line arguments"""
    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"

    # get environment variables
    load_dotenv()

    # Check if OPENAI_API_KEY and OPENAI_API_BASE are set. If not set interactively ask for them and set them as environment variables
    if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("OPENAI_API_BASE"):
        print("Please set the following environment variables: OPENAI_API_KEY, OPENAI_API_BASE inorder to use this script.")
        return

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_base = os.environ.get("OPENAI_API_BASE")

    if not args:
        args = sys.argv[1:]
    
    user_prompt = ' '.join(args)
    
    messages = construct_message_with_history(user_prompt)
    return get_chat_completion(messages)
