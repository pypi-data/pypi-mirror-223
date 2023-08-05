import msgpack
import zmq
from dataclasses import asdict
from .schema.completion import Completion, CompletionChoice
from .schema.request import Request



class LlamaClient:

    def __init__(self, host: str):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(host)

    def send_request(self, request: Request) -> Completion:
        request_dict = asdict(request)
        packed_request = msgpack.packb(request_dict)
        self.socket.send(packed_request)
        response = self.socket.recv()
        return self.unpack_response(response)

    @staticmethod
    def unpack_response(packed_response: bytes) -> Completion:
        unpacker = msgpack.Unpacker(raw=False)
        unpacker.feed(packed_response)

        deserialized_data = []
        for obj in unpacker:
            deserialized_data.append(obj)
        
        response_dict = deserialized_data[-1]
        response_dict['choices'] = [CompletionChoice(**choice) for choice in response_dict['choices']]
        return Completion(**response_dict)
