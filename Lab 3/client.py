import grpc
from grpc._channel import _InactiveRpcError
import reverse_pb2
import reverse_pb2_grpc


channel = grpc.insecure_channel('localhost:50051')
stub = reverse_pb2_grpc.ReverseStub(channel)


while True:
    string = input("Enter message to reverse ('end' to finish) >> ")
    if string == 'end':
        break
    try:
        request = reverse_pb2.Message(text=string)
        response = stub.reverse(request)
        print("Reversed message: ", response.text)
    except _InactiveRpcError:
        print("Lost connection with server. Please, wait or enter 'end' to finish")
