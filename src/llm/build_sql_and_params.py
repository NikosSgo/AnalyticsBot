from datetime import datetime, timedelta, time
import re
from typing import Dict, Any
from typing import List

from dateutil.parser import parse

from .functions import QUERY_DEFINITIONS


def _is_date_only(value: Any) -> bool:
    if isinstance(value, str):
        return ":" not in value and "T" not in value
    return False


def normalize_dates(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Приводит date / date_from / date_to к datetime для SQL.
    Использует поле 'inclusive', которое присылает LLM.
    """
    params = dict(params)

    if "date" in params:
        dt = parse(params["date"])
        if dt.time() == time.min:
            date_from = datetime.combine(dt.date(), time.min)
            date_to = date_from + timedelta(days=1)
        else:
            date_from = dt
            date_to = dt
        params["date_from"] = date_from
        params["date_to"] = date_to
        del params["date"]

    if "date_from" in params or "date_to" in params:
        inclusive = params.get("inclusive", False)

        if "date_from" in params and params["date_from"] is not None:
            from_dt = parse(params["date_from"])
            if from_dt.time() == time.min and _is_date_only(params["date_from"]):
                from_dt = datetime.combine(from_dt.date(), time.min)
            params["date_from"] = from_dt

        if "date_to" in params and params["date_to"] is not None:
            to_dt = parse(params["date_to"])
            if to_dt.time() == time.min and _is_date_only(params["date_to"]):
                to_dt = datetime.combine(to_dt.date(), time.min)
                if inclusive:
                    to_dt += timedelta(days=1)
            params["date_to"] = to_dt

        params.pop("inclusive", None)

    return params


def parse_param_value(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return parse(value)
        except:
            return value
    return value


def _max_sql_param_index(sql: str) -> int:
    matches = re.findall(r"\$(\d+)", sql)
    if not matches:
        return 0
    return max(int(m) for m in matches)


def build_sql_and_params(query_name: str, params: Dict[str, Any]) -> tuple[str, List[Any]]:
    query_def = QUERY_DEFINITIONS[query_name]
    sql = query_def["sql"]
    params = normalize_dates(params)
    param_names = list(query_def.get("parameters", {}).keys())
    # "date" and "inclusive" are helper params used only for normalization.
    param_names = [name for name in param_names if name not in {"date", "inclusive"}]

    sql_params = [parse_param_value(params.get(name)) for name in param_names]
    max_param_index = _max_sql_param_index(sql)
    if max_param_index:
        sql_params = sql_params[:max_param_index]
    else:
        sql_params = []
    return sql, sql_params
