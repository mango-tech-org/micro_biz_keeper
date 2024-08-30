# Define the source directory and target directory
PROTO_SRC_DIR = ./auth_service/grpc_pb
PROTO_TARGET_DIR = ./auth_service/grpc_pb

# Define the .proto file to be compiled
PROTO_FILE = $(PROTO_SRC_DIR)/auth.proto

# Define the Python modules output locations
PYTHON_OUT = --python_out=$(PROTO_TARGET_DIR)
GRPC_PYTHON_OUT = --grpc_python_out=$(PROTO_TARGET_DIR)

# Command to run the gRPC code generation
generate_grpc:
	python -m grpc_tools.protoc -I$(PROTO_SRC_DIR) $(PYTHON_OUT) $(GRPC_PYTHON_OUT) $(PROTO_FILE)

# Clean up generated files
clean:
	rm -f $(PROTO_TARGET_DIR)/*_pb2.py $(PROTO_TARGET_DIR)/*_pb2_grpc.py
