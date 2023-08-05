from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal
from .request import Message


@dataclass
class CompletionLogprobs:
    text_offset: List[int]
    token_logprobs: List[Optional[float]]
    tokens: List[str]
    top_logprobs: List[Optional[Dict[str, float]]]


@dataclass
class CompletionChoice:
    index: int
    message: Message
    logprobs: Optional[CompletionLogprobs]
    finish_reason: Optional[str]


@dataclass
class CompletionUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class Completion:
    id: str
    object: Literal["text_completion"]
    created: int
    choices: List[CompletionChoice]
    usage: CompletionUsage
    custom_props: dict[any:any] = field(default_factory=dict)