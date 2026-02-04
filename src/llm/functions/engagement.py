from typing import Dict

from .base import QueryDef

ENGAGEMENT_QUERY_DEFINITIONS: Dict[str, QueryDef] = {
    "count_videos_likes_gt": {
        "description": "Считает видео с лайками больше указанного числа",
        "sql": "SELECT COUNT(*) FROM videos WHERE likes_count > $1 AND ($2::timestamp IS NULL OR video_created_at >= $2::timestamp) AND ($3::timestamp IS NULL OR video_created_at < $3::timestamp);",
        "parameters": {
            "likes_gt": {"type": "integer", "description": "Минимальное число лайков"},
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": ["likes_gt"]
    },

    "count_videos_comments_gt": {
        "description": "Считает видео с комментариями больше указанного числа",
        "sql": "SELECT COUNT(*) FROM videos WHERE comments_count > $1 AND ($2::timestamp IS NULL OR video_created_at >= $2::timestamp) AND ($3::timestamp IS NULL OR video_created_at < $3::timestamp);",
        "parameters": {
            "comments_gt": {"type": "integer", "description": "Минимальное число комментариев"},
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": ["comments_gt"]
    },

    "sum_delta_likes_by_date": {
        "description": "Суммирует прирост лайков за день",
        "sql": "SELECT COALESCE(SUM(delta_likes_count), 0) FROM video_snapshots WHERE ($1::timestamp IS NULL OR created_at >= $1::timestamp) AND ($2::timestamp IS NULL OR created_at < $2::timestamp);",
        "parameters": {
            "date_from": {"type": "string", "description": "Дата начала (YYYY-MM-DD или ISO datetime)"},
            "date_to": {"type": "string", "description": "Дата окончания (YYYY-MM-DD или ISO datetime)"},
            "date": {"type": "string", "description": "Конкретная дата (YYYY-MM-DD или ISO datetime)"},
            "inclusive": {"type": "boolean", "description": "Включительно ли date_to (только если date_to — дата без времени)"}
        },
        "required": []
    },
}
