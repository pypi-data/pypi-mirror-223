from python_web_io.cache import cache_to_file
from python_web_io.override import RunPyInterrupt

import pkg_resources
from fastapi.templating import Jinja2Templates

# Get the path to the templates directory within your package
templates_path = pkg_resources.resource_filename(__name__, "templates")

# Create Jinja2Templates instance with the templates directory
templates = Jinja2Templates(directory=templates_path)