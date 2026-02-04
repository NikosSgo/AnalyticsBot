from typing import Dict

from .base import QueryDef

VIDEO_CREATOR_QUERY_DEFINITIONS: Dict[str, QueryDef] = {
    # Видео конкретного креатора
    "count_videos_by_creator": {
        "description": "Считает общее количество видео конкретного автора",
        "sql": "SELECT COUNT(*) FROM videos WHERE creator_id = $1 AND ($2 IS NULL OR video_created_at >= $2) AND ($3 IS NULL OR video_created_at < $3);",
        "parameters": {
            "creator_id": {"type": "string", "description": "ID автора"},
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": ["creator_id"]
    },

    # Видео креатора за период
    "count_videos_by_creator_date_range": {
        "description": "Считает видео автора за указанный период",
        "sql": "SELECT COUNT(*) FROM videos WHERE creator_id = $1 AND ($2 IS NULL OR video_created_at >= $2) AND ($3 IS NULL OR video_created_at < $3);",
        "parameters": {
            "creator_id": {"type": "string", "description": "ID автора"},
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": ["creator_id"]
    },
}
