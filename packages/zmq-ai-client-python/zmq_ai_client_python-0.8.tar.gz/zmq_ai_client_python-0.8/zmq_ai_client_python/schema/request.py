from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Message:
    role: str
    content: str
    name: Optional[str] = None
    function_call: Optional[dict] = None

@dataclass
class Function:
    name: str
    description: Optional[str] = None
    parameters: Optional[dict] = None
    function_call: Optional[str] = None

@dataclass
class Request:
    model: str
    messages: List[Message]
    functions: Optional[List[Function]] = None
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[str] = None
    max_tokens: Optional[int] = 256
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[dict] = None
    user: Optional[str] = None