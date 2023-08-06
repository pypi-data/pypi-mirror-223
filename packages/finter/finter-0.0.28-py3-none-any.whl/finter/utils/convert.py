import numpy as np
import pandas as pd
import json


def str_to_type(type_str):
    if type_str == "str":
        return str
    elif type_str == "int":
        return int
    elif type_str == "float":
        return float
    # 여기에 필요한 다른 타입들을 추가하세요.
    else:
        return str


def to_dataframe(json_response, column_types=None):
    try:
        df = pd.DataFrame.from_dict(json.loads(json_response), orient='index')
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.applymap(lambda x: np.nan if x is None else x)
        if column_types:
            if isinstance(column_types, str):
                column_types = json.loads(column_types)
            response_column_types = pd.Series(column_types)
            df.columns = df.columns.to_series().apply(lambda x: str_to_type(response_column_types.loc[str(x)])(x))
        return df
    except Exception as e:
        print(e)
        return pd.read_json(json_response, orient='index')
