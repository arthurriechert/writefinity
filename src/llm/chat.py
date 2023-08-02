from typing import List, Generator, TypedDict
from dataclasses import dataclass
import os
import json

import openai
import tiktoken

class Message(TypedDict):
    role: str
    content: str

@dataclass
class Settings:
    make: str
    model: str
    temperature: float
    max_tokens: int
    token_proportions: dict
    perogative: dict

class ChatInstance:
    def __init__(self, seed: List[Message], api_key: str, settings_path: str = "settings.json"):
        self.history = seed
        openai.api_key = api_key

        with open(settings_path, 'r') as file:
            self.settings = Settings(**json.load(file)["chat"])

        self.history.append(self.settings.perogative)

        self.encoder = tiktoken.encoding_for_model(self.settings.model)
        self.token_count = self.count_tokens(seed)

    def __getitem__(self, index) -> Message:
        return self.history[index]
    
    def count_tokens(self, message_list: List[Message]) -> int:
        return len(self.encoder.encode("\n".join([message["content"] for message in message_list])))
    
    def token_percentage_of_max(self, multiplier: float) -> int:
        assert 0.0 <= multiplier <= 1.0, "Multiplier may only be between 1 or 0."
        return int(multiplier * self.settings.max_tokens)
    
    @property
    def completion_allocation(self):
        return int(self.token_percentage_of_max(self.settings.token_proportions["completions"]))
    
    @property
    def history_allocation(self):
        return int(self.token_percentage_of_max(self.settings.token_proportions["history"]))
    
    def reset(self) -> None:
        del self.history[3:]
        self.token_count = self.count_tokens(self.history[:2])
    
    def get_completion(self, user_content: str) -> str:
            
        formatted_user_message = Message (
            role="user", 
            content=user_content
        )

        self.history.append(formatted_user_message)

        assistant_content = ""
        assistant_content = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=self.history,
            temperature=self.settings.temperature,
            max_tokens=self.completion_allocation,
        )["choices"][0]["message"]["content"]

        formatted_assistant_message = Message (
            role="assistant", 
            content=assistant_content
        )

        self.history.append(formatted_assistant_message)

        self.token_count += self.count_tokens([formatted_user_message, formatted_assistant_message])

        return assistant_content

    def stream_completion(self, user_content: str) -> Generator[str, None, None]:
        
        formatted_user_message = Message (
            role="user", 
            content=user_content
        )

        self.history.append(formatted_user_message)

        assistant_content = ""
        for chunk in openai.ChatCompletion.create(
            model=self.settings.model,
            messages=self.history,
            temperature=self.settings.temperature,
            max_tokens=self.completion_allocation,
            stream=True,
        ):
            delta = chunk.choices[0].delta.get("content", "")
            assistant_content += delta
            yield delta

        formatted_assistant_message = Message (
            role="assistant", 
            content=assistant_content
        )

        self.history.append(formatted_assistant_message)

        self.token_count += self.count_tokens([formatted_user_message, formatted_assistant_message])