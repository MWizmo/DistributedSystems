import grpc
from concurrent import futures
import time
import reverse_pb2
import reverse_pb2_grpc


class ReverseServicer(reverse_pb2_grpc.ReverseServicer):
    def reverse(self, request, context):
        response = reverse_pb2.Message(text=request.text[::-1])
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
reverse_pb2_grpc.add_ReverseServicer_to_server(ReverseServicer(), server)
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    server.stop(0)
