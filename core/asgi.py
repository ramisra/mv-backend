import sys
from pathlib import Path

import uvicorn

from core.app import create_app
from core.config import get_settings

# Get the absolute path of the directory containing this script
current_file = Path(__file__).resolve()
parent_directory = current_file.parent
project_directory = parent_directory.parent

sys.path.insert(0, str(project_directory))

app = create_app(get_settings())


if __name__ == "__main__":
    uvicorn.run("core.asgi:app", host="0.0.0.0", port=8000, reload=True)
