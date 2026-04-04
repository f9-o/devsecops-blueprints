import httpx
from typing import Generator, Tuple

BASE_URL = "https://raw.githubusercontent.com/f9-o/devsecops-blueprints/main/blueprints"

def stream_blueprint(template_name: str) -> Generator[Tuple[bytes, int, int], None, None]:
    """
    Streams a blueprint file mapping its chunks and total size.
    Yields (chunk_bytes, chunk_size, total_size).
    Raises ValueError on Http 404.
    Raises ConnectionError on network failures.
    """
    url = f"{BASE_URL}/{template_name}/Dockerfile"
    try:
        # We use a httpx client to stream the response for showing progress UI cleanly
        with httpx.Client() as client:
            with client.stream("GET", url) as response:
                if response.status_code == 404:
                    raise ValueError(f"Blueprint '{template_name}' not found in the armory.")
                response.raise_for_status()
                
                total_size = int(response.headers.get("content-length", 0))
                # Iter chunks
                for chunk in response.iter_bytes(chunk_size=1024):
                    yield chunk, len(chunk), total_size
    except httpx.RequestError as e:
        raise ConnectionError(f"Network error while fetching blueprint: {str(e)}")
