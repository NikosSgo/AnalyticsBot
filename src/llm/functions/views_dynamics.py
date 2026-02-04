from typing import Dict

from .base import QueryDef

VIEWS_DYNAMICS_QUERY_DEFINITIONS: Dict[str, QueryDef] = {
    # Сумма прироста просмотров за день
    "sum_delta_views_by_date": {
        "description": "Суммирует прирост просмотров за конкретную дату",
        "sql": "SELECT COALESCE(SUM(delta_views_count), 0) FROM video_snapshots WHERE ($1::timestamp IS NULL OR created_at >= $1::timestamp) AND ($2::timestamp IS NULL OR created_at < $2::timestamp);",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },

    # Количество видео с приростом просмотров за день
    "count_videos_with_delta_views_by_date": {
        "description": "Считает уникальные видео, получившие новые просмотры за день",
        "sql": "SELECT COUNT(DISTINCT video_id) FROM video_snapshots WHERE delta_views_count > 0 AND ($1::timestamp IS NULL OR created_at >= $1::timestamp) AND ($2::timestamp IS NULL OR created_at < $2::timestamp);",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },

    # Сумма прироста просмотров за период
    "sum_delta_views_by_date_range": {
        "description": "Суммирует прирост просмотров за период",
        "sql": "SELECT COALESCE(SUM(delta_views_count), 0) FROM video_snapshots WHERE ($1::timestamp IS NULL OR created_at >= $1::timestamp) AND ($2::timestamp IS NULL OR created_at < $2::timestamp);",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },
}
