import requests

from foreverbull.models.service import SocketConfig

from .http import api_call


@api_call
def create(name: str, image: str) -> requests.Request:
    return requests.Request(
        method="POST",
        url="/api/v1/services",
        json={"name": name, "image": image},
    )


@api_call
def get(service: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/services/{service}",
    )


@api_call
def update_instance(container_id: str, socket: SocketConfig = None) -> requests.Request:
    return requests.Request(
        method="PATCH",
        url=f"/api/v1/services/instances/{container_id}",
        json={**socket.model_dump()} if socket else {},
    )
