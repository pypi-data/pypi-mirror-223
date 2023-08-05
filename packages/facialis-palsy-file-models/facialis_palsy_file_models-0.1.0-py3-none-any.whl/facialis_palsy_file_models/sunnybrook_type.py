from typing import Optional, List

from pydantic import BaseModel, validator, ConfigDict

from .base_types import KeyValue


class Sunnybrook(BaseModel):
    metadata_object_version: str = "0.1.0"
    application_version: str = "APPLICATION_VERSION"
    application_org: str = "ORGANIZATION_DOMAIN"

    #model_config = ConfigDict(allow_mutation=True)
    #'allow_mutation' has been removed

    # static
    rest_eye: Optional[KeyValue] = None,
    rest_cheek: Optional[KeyValue] = None,  # nasolabial
    rest_mouth: Optional[KeyValue] = None,
    # dynamic
    frowning_symmetry: Optional[KeyValue] = None,  # brow lift
    gentleeye_symmetry: Optional[KeyValue] = None,
    dental_symmetry: Optional[KeyValue] = None,  # smile
    snarl_symmetry: Optional[KeyValue] = None,
    lippucker_symmetry: Optional[KeyValue] = None,  # mouth pursing
    # synkinesis
    frowning_synkinesis: Optional[KeyValue] = None,  # brow lift
    gentleeye_synkinesis: Optional[KeyValue] = None,
    dental_synkinesis: Optional[KeyValue] = None,  # smile
    snarl_synkinesis: Optional[KeyValue] = None,
    lippucker_synkinesis: Optional[KeyValue] = None,  # mouth pursing

    time_series: Optional[List[KeyValue]] = []

    @validator("time_series", pre=True)
    def check_pre_unpack(cls, x):
        # the "*" validator unpacks lists, and so it
        # unpacks also the time series, wich has to be a list...
        return x

    @validator("*", pre=True)
    def check_unpack_list(cls, x):
        if isinstance(x, list) and len(x) == 1:
            x = x[0]
        if x == "null" or x is None:
            return None
        else:
            return x

    def __init__(self, **data) -> None:
        super().__init__(**data)
        # self.__config__.allow_mutation = True

    def total_score_resting(self):
        values = [self.rest_cheek, self.rest_eye, self.rest_mouth]
        try:
            return 5 * sum([int(v.value) for v in values])
        except AttributeError:
            raise ValueError("Some rest values are not set.")

    def total_score_symmetry_voluntary_movement(self):
        values = [
            self.frowning_symmetry,
            self.gentleeye_symmetry,
            self.dental_symmetry,
            self.snarl_symmetry,
            self.lippucker_symmetry
        ]
        try:
            return 4 * sum([int(v.value) for v in values])
        except AttributeError:
            raise ValueError("Some symmetry voluntary movement values are not set.")

    def total_score_synkinesis(self):
        values = [
            self.frowning_synkinesis,
            self.gentleeye_synkinesis,
            self.dental_synkinesis,
            self.snarl_synkinesis,
            self.lippucker_synkinesis
        ]
        try:
            return 4 * sum([int(v.value) for v in values])
        except AttributeError:
            raise ValueError("Some synkinesis values are not set.")

    def total_score(self):
        return self.total_score_symmetry_voluntary_movement() \
               - self.total_score_resting() \
               - self.total_score_synkinesis()

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
        :return:
        # TODO #86 Missing Value
        """
        return [key for key, value in self.get_all_values().items() if value is None or isinstance(value, tuple)]

