from google.protobuf import __version__

if __version__.startswith("4"):
    from ._generated_pb4.service_test_pb2 import *
else:
    from ._generated_pb3.service_test_pb2 import *
