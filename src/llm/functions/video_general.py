from typing import Dict

from .base import QueryDef

VIDEO_GENERAL_QUERY_DEFINITIONS: Dict[str, QueryDef] = {
    # Общее количество
    "count_videos": {
        "description": "Возвращает общее число видео",
        "sql": "SELECT COUNT(*) FROM videos WHERE ($1 IS NULL OR video_created_at >= $1) AND ($2 IS NULL OR video_created_at < $2);",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },

    # Видео с просмотрами больше порога
    "count_videos_views_gt": {
        "description": "Считает видео с просмотрами больше указанного числа",
        "sql": "SELECT COUNT(*) FROM videos WHERE views_count > $1 AND ($2 IS NULL OR video_created_at >= $2) AND ($3 IS NULL OR video_created_at < $3);",
        "parameters": {
            "views_gt": {"type": "integer", "description": "Минимальное число просмотров"},
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": ["views_gt"]
    },

    # Видео за период по дате создания
    "count_videos_by_date_range": {
        "description": "Считает видео, опубликованные с даты по дату",
        "sql": "SELECT COUNT(*) FROM videos WHERE ($1 IS NULL OR video_created_at >= $1) AND ($2 IS NULL OR video_created_at < $2);",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },
}
