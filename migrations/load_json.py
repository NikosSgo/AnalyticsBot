import os
import asyncio
import asyncpg
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Iterable
from dotenv import load_dotenv

load_dotenv()

BATCH_SIZE = 1000


def chunked(iterable: list, size: int) -> Iterable[list]:
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


def parse_ts(value: str) -> datetime:
    # ISO 8601 с timezone → datetime
    return datetime.fromisoformat(value)


async def main(json_path: Path):

    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")

    dsn = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=1,
        max_size=5,
    )

    # === загрузка JSON ===
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    videos = data["videos"]

    async with pool.acquire() as conn:
        async with conn.transaction():

            video_rows = []
            snapshot_rows = []

            for video in videos:
                video_rows.append((
                    video["id"],
                    video["creator_id"],
                    parse_ts(video["video_created_at"]),
                    video["views_count"],
                    video["likes_count"],
                    video["comments_count"],
                    video["reports_count"],
                    parse_ts(video["created_at"]),
                    parse_ts(video["updated_at"]),
                ))

                for snap in video["snapshots"]:
                    snapshot_rows.append((
                        snap["id"],
                        snap["video_id"],
                        snap["views_count"],
                        snap["likes_count"],
                        snap["comments_count"],
                        snap["reports_count"],
                        snap["delta_views_count"],
                        snap["delta_likes_count"],
                        snap["delta_comments_count"],
                        snap["delta_reports_count"],
                        parse_ts(snap["created_at"]),
                        parse_ts(snap["updated_at"]),
                    ))

            insert_videos_sql = """
                INSERT INTO videos (
                    id,
                    creator_id,
                    video_created_at,
                    views_count,
                    likes_count,
                    comments_count,
                    reports_count,
                    created_at,
                    updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (id) DO NOTHING
            """

            for batch in chunked(video_rows, BATCH_SIZE):
                await conn.executemany(insert_videos_sql, batch)

            insert_snapshots_sql = """
                INSERT INTO video_snapshots (
                    id,
                    video_id,
                    views_count,
                    likes_count,
                    comments_count,
                    reports_count,
                    delta_views_count,
                    delta_likes_count,
                    delta_comments_count,
                    delta_reports_count,
                    created_at,
                    updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                ON CONFLICT (id) DO NOTHING
            """

            for batch in chunked(snapshot_rows, BATCH_SIZE):
                await conn.executemany(insert_snapshots_sql, batch)

    await pool.close()
    print("Загрузка завершена успешно.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python load_json.py <path_to_json>")
        sys.exit(1)

    asyncio.run(main(Path(sys.argv[1])))
