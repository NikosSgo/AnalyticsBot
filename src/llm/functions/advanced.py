from typing import Dict

from .base import QueryDef

ADVANCED_QUERY_DEFINITIONS: Dict[str, QueryDef] = {
    "count_videos_top_views_by_date_range": {
        "description": "Считает видео в топ-10 по приросту просмотров за день",
        "sql": "SELECT COUNT(*) FROM (SELECT video_id FROM video_snapshots WHERE ($1::timestamp IS NULL OR created_at >= $1::timestamp) AND ($2::timestamp IS NULL OR created_at < $2::timestamp) AND delta_views_count > 0 ORDER BY delta_views_count DESC LIMIT 10) t;",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },

    "count_active_creators_by_date_range": {
        "description": "Считает уникальных авторов с активностью за период",
        "sql": "SELECT COUNT(DISTINCT v.creator_id) FROM videos v JOIN video_snapshots s ON v.id = s.video_id WHERE ($1::timestamp IS NULL OR s.created_at >= $1::timestamp) AND ($2::timestamp IS NULL OR s.created_at < $2::timestamp) AND s.delta_views_count > 0;",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },
}
