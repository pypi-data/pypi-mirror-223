from .client import LlamaClient
from .schema.completion import Completion
from .schema.request import Message,Request

def main():
    client = LlamaClient('tcp://localhost:5555')

    messages = [
        Message(role='system', content='You are a helpful assistant.'),
        Message(role='user', content='What is the capital of france?'),
    ]

    request = Request(model='gpt-3.5-turbo', messages=messages, temperature=0.8, n=5)

    response:Completion = client.send_request(request)

    print(response)

if __name__ == "__main__":
    main()
