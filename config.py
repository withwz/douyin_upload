from pydantic import BaseModel
import os


class Config(BaseModel):

    _path: str = os.path.abspath("")

    video_path: str = os.path.join(_path, "video")


config = Config()
