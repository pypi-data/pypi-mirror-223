#!/usr/bin/env python3
import argparse
import json
import os

from atksh_utils.openai import OpenAI


def cb(chunk, message):
    if chunk["choices"][0]["finish_reason"] is not None:
        if chunk["choices"][0]["finish_reason"] == "stop":
            print("\n")
        else:
            info = chunk["choices"][0]
            if info["finish_reason"] == "function_call":
                function_name = message["function_call"]["name"]
                function_call_args = json.loads(message["function_call"]["arguments"])
                pretty_args = []
                for arg, value in function_call_args.items():
                    pretty_args.append(f"\t{arg}={value}")
                pretty_args = ",\n".join(pretty_args)
                text = f"{function_name}(\n{pretty_args}\n)"
                print("function_call:")
                print(text)
                print()
        return
    token = chunk["choices"][0]["delta"].get("content", "")
    if token:
        print(token, end="")


def setup_ai():
    key = os.getenv("OPENAI_API_KEY")
    ai = OpenAI(key, "gpt-4")
    ai.set_browser_functions()
    ai.set_exec_python_code_function()
    return ai


def ask():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="The query to ask to the AI.")
    ai = setup_ai()
    args = parser.parse_args()
    messages, _ = ai(args.query, stream_callback=cb, is_question=True)
    while True:
        user_prompt = input(">>> ")
        messages.append({"role": "user", "content": user_prompt})
        ai.call(user_prompt, stream_callback=cb, messages=messages)
