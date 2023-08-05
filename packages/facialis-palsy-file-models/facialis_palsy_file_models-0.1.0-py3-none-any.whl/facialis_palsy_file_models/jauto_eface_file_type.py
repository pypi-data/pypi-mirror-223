from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .eface_type import Eface
from .housebrackmann_type import HouseBrackmann
from .sunnybrook_type import Sunnybrook
from .utils import cleanup_characters_from


# TODO should be a jAuto-eface File Model, it describes the composed file.
class EfaceSunnybrookFile(BaseModel):
    metadata_object_version: str = "0.1.0"
    application_version: str = "APPLICATION_VERSION"
    application_org: str = "ORGANIZATION_DOMAIN"
    version: str = "v3_mh_2022"

    # model_config = ConfigDict(allow_mutation=True)
    #'allow_mutation' has been removed

    eface: Eface = Eface()
    sunnybrook: Sunnybrook = Sunnybrook()
    houseBrackmann: HouseBrackmann = HouseBrackmann()
    rater: str = ""
    filename: str = ""
    directory: str = None
    rating_start: str = ""
    rating_end: str = ""
    palsy_side: str = ""
    age: int = 0
    gender: str = ""
    r: str = ""
    image_names: List[str] = []
    image_quality: List[int] = []
    image_quality_description: Optional[List[List[str]]] = None
    pid: str = ""
    sunnybrook_score_rest: int = 0
    sunnybrook_score_volu: int = 0
    sunnybrook_score_synk: int = 0
    sunnybrook_score: int = 0

    # TODO großes Problem beim Laden von Dateien, aus anderen Dateisystemen!
    #  somit ist ein Validator an dieser Stelle nicht möglich. Sondern muss
    #  direkt in der Applikation erfolgen.
    """
    @validator("directory", always=True)
    def check_directory(cls, x):
        if isinstance(x, str):
            if os.path.exists(x):
                return x
            else:
                raise ValueError("directory doesn't exist.")
        if x == 'null' or x is None or x == 'nill':
            return None
        else:
            return x
    """

    def __init__(self, **data) -> None:
        super().__init__(**data)
        # self.__config__.allow_mutation = True
        self.rating_start = f"{datetime.now().timestamp()}"

    class Config:
        arbitrary_types_allowed = True

    def set_image_quality(self, index, value):
        self.image_quality[index] = value

    def set_image_quality_description(self, index: int, value: [str]):
        self.image_quality_description[index] = value

    def json(self, **kwargs):
        self.rating_end = f"{datetime.now().timestamp()}"
        return super(EfaceSunnybrookFile, self).json(**kwargs)

    def rater_filename(self):
        """
        get rater name as filename with:
        replaced unwanted characters from rater name
        :return:
        """
        name = f"{self.rater}"
        return cleanup_characters_from(name)

    @staticmethod
    def __date_format(timestamp):
        """
        format timestamp '%Y-%m-%d %H:%M'
        :param timestamp:
        :return:
        """
        return datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M')

    def rating_start_date(self):
        return self.__date_format(self.rating_start)

    def rating_end_date(self):
        return self.__date_format(self.rating_end)
