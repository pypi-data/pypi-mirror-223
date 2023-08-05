
from pydantic import BaseModel, validator, ConfigDict
from typing import Optional, List

from facialis_palsy_file_models.base_types import KeyValue


class Eface(BaseModel):
    metadata_object_version: str = "0.1.0"
    application_version: str = "APPLICATION_VERSION"
    application_org: str = "ORGANIZATION_DOMAIN"

    #model_config = ConfigDict(allow_mutation=True)
    # 'allow_mutation' has been removed

    # static scores
    rest_brow: Optional[int] = None,
    rest_palpebral: Optional[int] = None,  # fissure at rest
    rest_oral: Optional[int] = None,  # oral commissure at rest
    rest_nasolabialfold: Optional[int] = None,  # depth
    rest_nasolabialfoldorientation: Optional[int] = None,

    # dynamic scores
    frowning_brow: Optional[int] = None,
    gentleeye_dynamic: Optional[int] = None,
    fulleye_dynamic: Optional[int] = None,
    dental_oral: Optional[int] = None,  # oral commissure
    dental_nasolabialdepth: Optional[int] = None,
    dental_nasolabialorientation: Optional[int] = None,
    snarl_dynamic: Optional[int] = None,  # lower lip mit eeee

    # synkinesis scores
    frowning_ocular: Optional[int] = None,
    frowning_midfacial: Optional[int] = None,
    frowning_mentalis: Optional[int] = None,
    frowning_platysmal: Optional[int] = None,

    gentleeye_ocular: Optional[int] = None,
    gentleeye_midfacial: Optional[int] = None,
    gentleeye_mentalis: Optional[int] = None,
    gentleeye_platysmal: Optional[int] = None,

    fulleye_ocular: Optional[int] = None,
    fulleye_midfacial: Optional[int] = None,
    fulleye_mentalis: Optional[int] = None,
    fulleye_platysmal: Optional[int] = None,

    dental_ocular: Optional[int] = None,  # smile
    dental_midfacial: Optional[int] = None,
    dental_mentalis: Optional[int] = None,
    dental_platysmal: Optional[int] = None,

    snarl_ocular: Optional[int] = None,  # lower lip movement
    snarl_midfacial: Optional[int] = None,
    snarl_mentalis: Optional[int] = None,
    snarl_platysmal: Optional[int] = None,
    # Optional for allowance of None values in model
    # it would cause problems in export and import to json...

    time_series: Optional[List[KeyValue]] = []

    def __init__(self, **data) -> None:
        super().__init__(**data)
        # self.__config__.allow_mutation = True

    def get_all_values(self) -> dict:
        """
        all values as dict (helper function)
        :return:
        """
        return {key: value for key, value in self.dict().items()
                if key not in [
                    "time_series",
                    "metadata_object_version",
                    "jauto_eface_version",
                    "jauto_eface_org"
                ]}

    def get_all_values_as_list(self) -> list:
        """
        values as list like the old eface version.
        :return:
        """
        return [value for _, value in self.get_all_values().items()]

    def check_for_unchanged_values(self) -> list:
        """
        all key names with None vales (unchanged score values)
        # TODO #86 Missing Value
        :return:
        """
        return [key for key, value in self.get_all_values().items() if value is None or isinstance(value, tuple)]

    @validator("time_series", pre=True)
    def check_prevent(cls, x):
        # the "*" validator unpacks lists, and so it
        # unpacks also the time series, wich has to be a list...
        return x

    @validator("*", pre=True)
    def check_str(cls, x):
        if isinstance(x, list) and len(x) == 1:
            x = x[0]
        if x == 'null' or x is None or x == 'nill':
            return None
        else:
            return x
