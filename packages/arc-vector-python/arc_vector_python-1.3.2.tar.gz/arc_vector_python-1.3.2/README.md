## arc-vector-python
Python library and client for arc-vector database

## Installation
// arc_vector_python-<version>.tar.gz package exist in local
pip install arc_vector_python-1.3.2.tar.gz

## Connect to ArcVector Server
To connect to Qdrant server, simply specify host and port:

```
from arc_vector_client import ArcVectorClient
from arc_vector_client.models import Distance, VectorParams
# Rest interface
client = ArcVectorClient(url="http://localhost:6333")
# gRPC: To enable (typically, much faster) collection uploading with gRPC
client = ArcVectorClient(host="localhost", grpc_port=6334, prefer_grpc=True)
```

