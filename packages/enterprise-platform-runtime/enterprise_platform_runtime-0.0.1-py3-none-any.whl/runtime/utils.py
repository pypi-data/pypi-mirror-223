from datetime import datetime, timedelta
from uuid import UUID

_TYPE_MAP = {
    dict: "OBJECT",
    list: "ARRAY",
    tuple: "ARRAY",
    set: "ARRAY",
    float: "NUMBER",
    int: "NUMBER",
    bool: "BOOLEAN",
    str: "CHAR",
    UUID: "CHAR",
    datetime: "DATETIME",
    timedelta: "DURATION",
}


def render_for_platform(data):
    """
    This function is used to render data that is sent to the platform
    into a format that is more friendly for the platform. This is done by
    wrapping the data in a dict that contains the data_type of the data.
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if isinstance(value, dict):
                new_dict[key] = {
                    "value": render_for_platform(value),
                    "data_type": "OBJECT",
                }
            else:
                new_dict[key] = render_for_platform(value)
        return new_dict

    if isinstance(data, (list, tuple, set)):
        for i in range(len(data)):
            if isinstance(data[i], dict):
                data[i] = {
                    "value": render_for_platform(data[i]),
                    "data_type": "OBJECT",
                }
            else:
                data[i] = render_for_platform(data[i])
        return {"value": data, "data_type": "ARRAY"}

    if isinstance(data, UUID):
        return {"value": str(data), "data_type": "CHAR"}

    if isinstance(data, datetime):
        return {"value": data.isoformat(), "data_type": "DATETIME"}

    if isinstance(data, timedelta):
        return {"value": int(data.total_seconds()), "data_type": "DURATION"}

    if data is None:
        return {"value": None, "data_type": "UNDEFINED"}

    return {"value": data, "data_type": _TYPE_MAP[type(data)]}
