# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import reverse_pb2 as reverse__pb2


class ReverseStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.reverse = channel.unary_unary(
        '/Reverse/reverse',
        request_serializer=reverse__pb2.Message.SerializeToString,
        response_deserializer=reverse__pb2.Message.FromString,
        )


class ReverseServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def reverse(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ReverseServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'reverse': grpc.unary_unary_rpc_method_handler(
          servicer.reverse,
          request_deserializer=reverse__pb2.Message.FromString,
          response_serializer=reverse__pb2.Message.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Reverse', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
