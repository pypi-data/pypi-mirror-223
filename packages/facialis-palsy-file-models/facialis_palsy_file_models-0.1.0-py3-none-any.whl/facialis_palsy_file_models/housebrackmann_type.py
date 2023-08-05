from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from facialis_palsy_file_models.base_types import KeyValue


class HouseBrackmann(BaseModel):
    metadata_object_version: str = "0.1.0"
    application_version: str = "APPLICATION_VERSION"
    application_org: str = "ORGANIZATION_DOMAIN"

    # model_config = ConfigDict(allow_mutation=True)
    # 'allow_mutation' has been removed

    houseBrackmann: int = 0
    time_series: Optional[List[KeyValue]] = []

    _mapping = {
        "normal": 1,
        "Mild dysfunction": 2,
        "Moderate dysfunction": 3,
        "Moderately severe dysfunction": 4,
        "Severe dysfunction": 5,
        "Total paralysis": 6
    }
    _rome_mapping = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6
    }

    def set_house_brackmann(self, value: str):
        self.houseBrackmann = self.map_house_brackmann(value)

    def housebrackmann_from_description(self, description: str = None):
        if description is None:
            description = self.houseBrackmann
        return self.mapping.get(description)

    def map_house_brackmann(self, value: str):
        for hb_key, hb_value in self.mapping.items():
            try:
                hb_key = int(hb_key)
            except ValueError:
                pass
            try:
                hb_value = int(hb_value)
            except ValueError:
                pass
            if isinstance(hb_key, int) and isinstance(hb_value, str):
                if hb_value == value:
                    return hb_key
            elif isinstance(hb_key, str) and isinstance(hb_value, int):
                if hb_key == value:
                    return hb_value
            else:
                raise TypeError(f"key and value have mismatching types. "
                                f"{hb_key} ({type(hb_key)}): {hb_value} ({type(hb_value)})")

        return 0

    @property
    def mapping(self):
        return self._mapping

    @property
    def rome_mapping(self):
        return self._rome_mapping

    def __init__(self, **data) -> None:
        super().__init__(**data)
        # self.__config__.allow_mutation = True


    def check_for_unchanged_values(self):
        """
        return True if the time series quals 0.
        if the value has changed False gets returned.

        # TODO #86 check for missing values.
        :return:
        """
        if len(self.time_series) == 0:  # aktuell totaler blödsinn.
            return True
        else:
            return False

