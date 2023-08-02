from typing import TypedDict, List
import sys

from serpapi import GoogleSearch

sys.path.append("../")
from llm.chat import ChatInstance, Message

class DefaultOption(TypedDict):
    title: str
    link: str
    rank: int
    snippet: str

class Results(TypedDict):
    options: List[DefaultOption]

def create_context(llm: ChatInstance, context: str) -> str:
    cont

def organic_search(
    query: str, 
    context: str, 
    lang: str, 
    country: str, 
    api_key: str
) -> Results:
    serp = GoogleSearch({
        "q": query,
        "hl": lang,
        "gl": country,
        "api_key": api_key
    })

def filtered_search() -> Results:
    pass

def perform_search_operation(api_key: str) -> List[Message]:
    search_agent = ChatInstance([
        Message(role="")
    ])