import sys
from pathlib import Path

from core.app import create_app
from core.config import get_settings
# from core.crud.action import ActionCrud  # noqa: F401
# from core.models.schemas.input_output import JobInput  # noqa: F401

current_file = Path(__file__).resolve()
parent_directory = current_file.parent
project_directory = parent_directory.parent

sys.path.insert(0, str(project_directory))

app = create_app(get_settings())

from core.crud.job import JobCrud  # noqa: F401
from core.crud.user import UserCrud  # noqa: F401
from core.database import get_db_session  # noqa: F401
from core.models.action import Action  # noqa: F401
from core.models.job import Job, JobCreate  # noqa: F401
from core.models.user import User  # noqa: F401

db = next(get_db_session())
action = Action(id='b8bc9740-6e5f-428c-ae10-66acb5ccfe0e',
                  internal_function_name='video_captioning',
                  action_name='video_caption',
                  short_description='Caption your videos',
                  input_parameters=[{"key": "url",
                                     "type": "file_url",
                                     "description": "Your video URL",
                                     "required": True},
                                    {"key": "font_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "font_size",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "font_size",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "font",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "upper_case",
                                     "type": "boolean",
                                     "description": "",
                                     "required": False},
                                    {"key": "shadow_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "shadow_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "border_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "border_width",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "y_position",
                                     "type": "text",
                                     "description": "",
                                     "required": False}

                                    ]
               )

db.add(action)
db.commit()

#
# job_input = {
#         "key": "url",
#         "value": "https://www.youtube.com/watch?v=l0xlzSIl1Mk"
# }
#
# job_inputs = [JobInput(**job_input)]
#
# job_create_instance = JobCreate(
#     action_id=action.id,
#     inputs=job_inputs,
# )
#
# JobCrud.create_job(db, job_create_instance)
