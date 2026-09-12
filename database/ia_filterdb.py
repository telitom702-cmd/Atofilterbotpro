import asyncio
import base64
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta
from struct import pack
from typing import Dict, List, Optional, Tuple

from marshmallow import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from pyrogram.file_id import FileId
from umongo import Document, Instance, fields

from info import *
from utils import get_settings, save_group_settings


# =========================================================
# LOGGER
# =========================================================

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )
    logger.addHandler(handler)


# =========================================================
# DATABASE CONNECTION
# =========================================================

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

client2 = None
db2 = None
instance2 = None

if MULTIPLE_DB:
    client2 = AsyncIOMotorClient(DATABASE_URI2)
    db2 = client2[DATABASE_NAME]
    instance2 = Instance.from_db(db2)


# =========================================================
# GLOBAL CACHE
# =========================================================

_db_stats_cache = {
    "timestamp": None,
    "primary_size": 0.0,
}


# =========================================================
# DATABASE MODELS
# =========================================================

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute="_id")
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        collection_name = COLLECTION_NAME
        indexes = [
            "file_name",
        ]


if MULTIPLE_DB:

    @instance2.register
    class Media2(Document):
        file_id = fields.StrField(attribute="_id")
        file_ref = fields.StrField(allow_none=True)
        file_name = fields.StrField(required=True)
        file_size = fields.IntField(required=True)
        file_type = fields.StrField(allow_none=True)
        mime_type = fields.StrField(allow_none=True)
        caption = fields.StrField(allow_none=True)

        class Meta:
            collection_name = COLLECTION_NAME
            indexes = [
                "file_name",
            ]

else:
    Media2 = None


# =========================================================
# DATABASE SIZE
# =========================================================

async def check_db_size(database) -> float:
    """
    Return database size in MB.

    Includes:
    - dataSize
    - indexSize

    Cache duration: 10 minutes.
    """

    global _db_stats_cache

    try:
        now = datetime.utcnow()

        cache_timestamp = _db_stats_cache.get("timestamp")
        cached_size = _db_stats_cache.get("primary_size", 0.0)

        cache_is_valid = (
            cache_timestamp is not None
            and now - cache_timestamp < timedelta(minutes=10)
        )

        # Refresh immediately if cached size is near the limit
        if cache_is_valid and cached_size < 400:
            return cached_size

        stats = await database.command("dbstats")

        data_size = stats.get("dataSize", 0)
        index_size = stats.get("indexSize", 0)

        total_size_mb = (data_size + index_size) / (1024 * 1024)

        _db_stats_cache["primary_size"] = total_size_mb
        _db_stats_cache["timestamp"] = now

        logger.info(
            f"Database size: {total_size_mb:.2f} MB"
        )

        return total_size_mb

    except Exception:
        logger.exception("Error checking database size")
        return 0.0


# =========================================================
# FILE NAME CLEANER
# =========================================================

def clean_file_name(file_name: str) -> str:
    """
    Remove unnecessary special characters from file name.
    Keeps readable spaces between words.
    """

    if not file_name:
        return "Unknown File"

    file_name = str(file_name)

    file_name = re.sub(
        r"[_\-\.#+$%^&*()!~`,;:\"'?/<>\[\]{}=|\\]",
        " ",
        file_name,
    )

    file_name = re.sub(r"\s+", " ", file_name).strip()

    return file_name


# =========================================================
# SAVE FILE
# =========================================================

async def save_file(media) -> Tuple[bool, int]:
    """
    Save Telegram media file into MongoDB.

    Return values:
        (True, 1)  = Successfully saved
        (False, 0) = Duplicate file
        (False, 2) = Validation error
        (False, 3) = Other database error
    """

    file_name = getattr(media, "file_name", "Unknown File")

    try:
        file_id, file_ref = unpack_new_file_id(media.file_id)

        file_name = clean_file_name(file_name)

        # -------------------------------------------------
        # DUPLICATE CHECK IN PRIMARY DB
        # -------------------------------------------------

        primary_exists = await Media.find_one(
            {
                "_id": file_id
            }
        )

        if primary_exists:
            logger.info(
                f"[SKIP] '{file_name}' already exists in Primary DB."
            )
            return False, 0

        # -------------------------------------------------
        # DUPLICATE CHECK IN SECONDARY DB
        # -------------------------------------------------

        if MULTIPLE_DB and Media2 is not None:
            secondary_exists = await Media2.find_one(
                {
                    "_id": file_id
                }
            )

            if secondary_exists:
                logger.info(
                    f"[SKIP] '{file_name}' already exists in Secondary DB."
                )
                return False, 0

        # -------------------------------------------------
        # SELECT TARGET DATABASE
        # -------------------------------------------------

        save_media_model = Media
        target_db_name = "Primary"

        if MULTIPLE_DB and Media2 is not None:
            primary_db_size = await check_db_size(db)

            if primary_db_size >= 407:
                save_media_model = Media2
                target_db_name = "Secondary"

                logger.warning(
                    f"Primary DB size is {primary_db_size:.2f} MB. "
                    f"Saving file to Secondary DB."
                )

        # -------------------------------------------------
        # CAPTION
        # -------------------------------------------------

        caption = None

        if INDEX_CAPTION:
            media_caption = getattr(media, "caption", None)

            if media_caption:
                try:
                    caption = media_caption.html
                except Exception:
                    caption = str(media_caption)

        # -------------------------------------------------
        # FILE DATA
        # -------------------------------------------------

        file_size = getattr(media, "file_size", 0) or 0
        file_type = getattr(media, "file_type", None)
        mime_type = getattr(media, "mime_type", None)

        record = save_media_model(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=int(file_size),
            file_type=file_type,
            mime_type=mime_type,
            caption=caption,
        )

        # -------------------------------------------------
        # COMMIT
        # -------------------------------------------------

        await record.commit()

        logger.info(
            f"[SUCCESS] '{file_name}' saved to {target_db_name} DB."
        )

        return True, 1

    except ValidationError as error:
        logger.exception(
            f"[VALIDATION ERROR] '{file_name}' -> {error}"
        )
        return False, 2

    except DuplicateKeyError:
        logger.info(
            f"[SKIP] DuplicateKeyError: '{file_name}'"
        )
        return False, 0

    except Exception as error:
        logger.exception(
            f"[ERROR] Failed to save '{file_name}' -> {error}"
        )
        return False, 3


# =========================================================
# SEARCH REGEX BUILDER
# =========================================================

def build_search_regex(query):
    """
    Create a flexible regex for file search.

    Examples:
        KGF Chapter 2
        KGF.Chapter.2
        KGF-Chapter-2
        KGF_Chapter_2
    """

    if isinstance(query, list):
        valid_queries = [
            str(item).strip()
            for item in query
            if str(item).strip()
        ]

        if not valid_queries:
            return None

        raw_pattern = "|".join(
            re.escape(item)
            for item in valid_queries
        )

        return re.compile(
            raw_pattern,
            re.IGNORECASE,
        )

    query = str(query).strip()

    if not query:
        return None

    words = query.split()

    if len(words) > 1:
        raw_pattern = r"[\s._+\-()]*".join(
            re.escape(word)
            for word in words
        )
    else:
        raw_pattern = re.escape(query)

    try:
        return re.compile(
            raw_pattern,
            re.IGNORECASE,
        )
    except re.error:
        return None


# =========================================================
# SEARCH RESULTS
# =========================================================

async def get_search_results(
    chat_id,
    query,
    file_type=None,
    max_results=None,
    offset=0,
    filter=False,
):
    """
    Search files from Primary and Secondary DB.
    """

    # -----------------------------------------------------
    # GROUP SETTINGS
    # -----------------------------------------------------

    if chat_id is not None:
        settings = await get_settings(int(chat_id))

        if max_results is None:
            try:
                max_results = (
                    10
                    if settings.get("max_btn")
                    else int(MAX_B_TN)
                )
            except (KeyError, TypeError, ValueError):
                await save_group_settings(
                    int(chat_id),
                    "max_btn",
                    True,
                )

                settings = await get_settings(int(chat_id))

                max_results = (
                    10
                    if settings.get("max_btn")
                    else int(MAX_B_TN)
                )

    if max_results is None:
        max_results = 10

    max_results = max(1, int(max_results))
    offset = max(0, int(offset))

    # -----------------------------------------------------
    # BUILD REGEX
    # -----------------------------------------------------

    regex = build_search_regex(query)

    if regex is None:
        return [], None, 0

    if USE_CAPTION_FILTER:
        filter_mongo = {
            "$or": [
                {
                    "file_name": regex
                },
                {
                    "caption": regex
                },
            ]
        }
    else:
        filter_mongo = {
            "file_name": regex
        }

    if file_type:
        filter_mongo["file_type"] = file_type

    # =====================================================
    # ULTRA FAST MODE
    # =====================================================

    if ULTRA_FAST_MODE:
        limit = max_results + 1

        find_tasks = [
            Media.find(filter_mongo)
            .sort("$natural", -1)
            .skip(offset)
            .limit(limit)
            .to_list(length=limit)
        ]

        if MULTIPLE_DB and Media2 is not None:
            find_tasks.append(
                Media2.find(filter_mongo)
                .sort("$natural", -1)
                .skip(offset)
                .limit(limit)
                .to_list(length=limit)
            )

        results = await asyncio.gather(*find_tasks)

        files = []

        for result in results:
            files.extend(result)

        files = files[:limit]

        has_next_page = len(files) > max_results

        if has_next_page:
            files = files[:max_results]

        next_offset = (
            offset + len(files)
            if has_next_page
            else ""
        )

        total_results = (
            offset
            + len(files)
            + (1 if has_next_page else 0)
        )

        return files, next_offset, total_results

    # =====================================================
    # NORMAL MODE
    # =====================================================

    count_tasks = [
        Media.count_documents(filter_mongo)
    ]

    find_tasks = [
        Media.find(filter_mongo)
        .sort("$natural", -1)
        .skip(offset)
        .limit(max_results)
        .to_list(length=max_results)
    ]

    if MULTIPLE_DB and Media2 is not None:
        count_tasks.append(
            Media2.count_documents(filter_mongo)
        )

        find_tasks.append(
            Media2.find(filter_mongo)
            .sort("$natural", -1)
            .skip(offset)
            .limit(max_results)
            .to_list(length=max_results)
        )

    count_results, find_results = await asyncio.gather(
        asyncio.gather(*count_tasks),
        asyncio.gather(*find_tasks),
    )

    total_results = sum(count_results)

    files = []

    for result in find_results:
        files.extend(result)

    files = files[:max_results]

    next_offset = offset + len(files)

    if next_offset >= total_results:
        next_offset = ""

    return files, next_offset, total_results


# =========================================================
# BAD FILE SEARCH
# =========================================================

async def get_bad_files(query, file_type=None):
    """
    Search files using boundary-friendly regex.
    """

    query = str(query).strip()

    if not query:
        raw_pattern = r"."
    elif " " not in query:
        raw_pattern = (
            r"(\b|[\s._+\-()])"
            + re.escape(query)
            + r"(\b|[\s._+\-()])"
        )
    else:
        words = [
            re.escape(word)
            for word in query.split()
        ]

        raw_pattern = r"[\s._+\-()]*".join(words)

    try:
        regex = re.compile(
            raw_pattern,
            re.IGNORECASE,
        )
    except re.error:
        return [], 0

    if USE_CAPTION_FILTER:
        filter_mongo = {
            "$or": [
                {
                    "file_name": regex
                },
                {
                    "caption": regex
                },
            ]
        }
    else:
        filter_mongo = {
            "file_name": regex
        }

    if file_type:
        filter_mongo["file_type"] = file_type

    # -----------------------------------------------------
    # PRIMARY DB
    # -----------------------------------------------------

    cursor1 = (
        Media.find(filter_mongo)
        .sort("$natural", -1)
    )

    files1 = await cursor1.to_list(
        length=await Media.count_documents(filter_mongo)
    )

    files = list(files1)

    # -----------------------------------------------------
    # SECONDARY DB
    # -----------------------------------------------------

    if MULTIPLE_DB and Media2 is not None:
        cursor2 = (
            Media2.find(filter_mongo)
            .sort("$natural", -1)
        )

        files2 = await cursor2.to_list(
            length=await Media2.count_documents(filter_mongo)
        )

        files.extend(files2)

    total_results = len(files)

    return files, total_results


# =========================================================
# GET FILE DETAILS
# =========================================================

async def get_file_details(query):
    """
    Get a file by its database _id.
    """

    if not query:
        return None

    file_id = str(query)

    filter_mongo = {
        "_id": file_id
    }

    tasks = [
        Media.find(
            filter_mongo
        ).to_list(length=1)
    ]

    if MULTIPLE_DB and Media2 is not None:
        tasks.append(
            Media2.find(
                filter_mongo
            ).to_list(length=1)
        )

    results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            return result[0]

    return None


# =========================================================
# ENCODE FILE ID
# =========================================================

def encode_file_id(s: bytes) -> str:
    """
    Encode Telegram file ID.
    """

    result = b""
    zero_count = 0

    for byte in s + bytes([22]) + bytes([4]):
        if byte == 0:
            zero_count += 1
        else:
            if zero_count:
                result += b"\x00" + bytes([zero_count])
                zero_count = 0

            result += bytes([byte])

    return base64.urlsafe_b64encode(
        result
    ).decode().rstrip("=")


# =========================================================
# ENCODE FILE REFERENCE
# =========================================================

def encode_file_ref(file_ref: bytes) -> str:
    """
    Encode Telegram file reference.
    """

    return base64.urlsafe_b64encode(
        file_ref
    ).decode().rstrip("=")


# =========================================================
# UNPACK NEW FILE ID
# =========================================================

def unpack_new_file_id(new_file_id):
    """
    Return:
        file_id, file_ref
    """

    decoded = FileId.decode(new_file_id)

    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash,
        )
    )

    file_ref = encode_file_ref(
        decoded.file_reference
    )

    return file_id, file_ref


# =========================================================
# FETCH LATEST MEDIA
# =========================================================

async def dreamxbotz_fetch_media(limit: int) -> List:
    """
    Fetch latest media files.

    When Primary DB reaches the limit,
    fetch files from Secondary DB.
    """

    try:
        limit = max(1, int(limit))

        if MULTIPLE_DB and Media2 is not None:
            primary_db_size = await check_db_size(db)

            if primary_db_size >= 407:
                cursor = (
                    Media2.find()
                    .sort("$natural", -1)
                    .limit(limit)
                )

                return await cursor.to_list(
                    length=limit
                )

        cursor = (
            Media.find()
            .sort("$natural", -1)
            .limit(limit)
        )

        return await cursor.to_list(
            length=limit
        )

    except Exception:
        logger.exception(
            "Error fetching latest media"
        )
        return []


# =========================================================
# CLEAN TITLE
# =========================================================

async def dreamxbotz_clean_title(
    filename: str,
    is_series: bool = False,
) -> str:
    """
    Convert filename into a clean readable title.
    """

    try:
        if not filename:
            return "Unknown"

        filename = str(filename).strip()

        # -------------------------------------------------
        # Remove file extension
        # -------------------------------------------------

        filename = re.sub(
            r"\.(mkv|mp4|avi|mov|wmv|webm|ts)$",
            "",
            filename,
            flags=re.IGNORECASE,
        )

        # -------------------------------------------------
        # Series title extraction
        # -------------------------------------------------

        if is_series:
            series_match = re.search(
                r"^(.*?)(?:"
                r"S(\d{1,2})"
                r"|Season\s*(\d{1,2})"
                r")"
                r"(?:\s*E(?:pisode)?\s*\d{1,3})?"
                r"(?:\s*Combined)?",
                filename,
                re.IGNORECASE,
            )

            if series_match:
                title = series_match.group(1).strip()

                season = (
                    series_match.group(2)
                    or series_match.group(3)
                )

                title = re.sub(
                    r"[@._\-\[\](){}]+",
                    " ",
                    title,
                )

                title = re.sub(
                    r"\s+",
                    " ",
                    title,
                ).strip().title()

                if season:
                    return f"{title} S{int(season):02d}"

        # -------------------------------------------------
        # Remove year and everything after year
        # -------------------------------------------------

        year_match = re.search(
            r"^(.*?)(?:\s*\(?((?:19|20)\d{2})\)?)",
            filename,
            re.IGNORECASE,
        )

        if year_match:
            title = year_match.group(1).strip()
        else:
            title = filename

        # -------------------------------------------------
        # Remove common release tags
        # -------------------------------------------------

        title = re.sub(
            r"\b("
            r"480p|576p|720p|1080p|2160p|4k|"
            r"WEB[- .]?DL|WEBRip|BluRay|BRRip|"
            r"HDTV|HDRip|DVDRip|CAM|HDTC|"
            r"x264|x265|HEVC|AAC|DDP|DD|"
            r"Dual Audio|Hindi|English|Bengali|"
            r"Tamil|Telugu|Malayalam|Korean|"
            r"Season|Episode"
            r")\b.*$",
            "",
            title,
            flags=re.IGNORECASE,
        )

        title = re.sub(
            r"[@._\-\[\](){}]+",
            " ",
            title,
        )

        title = re.sub(
            r"\s+",
            " ",
            title,
        ).strip().title()

        return title or filename

    except Exception:
        logger.exception(
            "Error cleaning title"
        )
        return filename


# =========================================================
# GET MOVIES
# =========================================================

async def dreamxbotz_get_movies(
    limit: int = 20,
) -> List[str]:
    """
    Return movie titles from latest indexed files.
    """

    try:
        limit = max(1, int(limit))

        cursor = await dreamxbotz_fetch_media(
            limit * 3
        )

        results = set()

        series_pattern = re.compile(
            r"(?:"
            r"S\d{1,2}"
            r"|Season\s*\d+"
            r"|Season\d+"
            r")"
            r"(?:\s*Combined)?"
            r"(?:"
            r"E\d{1,3}"
            r"|Episode\s*\d+"
            r")?",
            re.IGNORECASE,
        )

        for file in cursor:
            file_name = getattr(
                file,
                "file_name",
                "",
            )

            if not file_name:
                continue

            # Skip series files
            if series_pattern.search(file_name):
                continue

            title = await dreamxbotz_clean_title(
                file_name
            )

            if title:
                results.add(title)

            if len(results) >= limit:
                break

        return sorted(results)[:limit]

    except Exception:
        logger.exception(
            "Error getting movie list"
        )
        return []


# =========================================================
# GET SERIES
# =========================================================

async def dreamxbotz_get_series(
    limit: int = 30,
) -> Dict[str, List[int]]:
    """
    Return series grouped by title and season.

    Example:
        {
            "The Glory": [1, 2],
            "Squid Game": [1]
        }
    """

    try:
        limit = max(1, int(limit))

        cursor = await dreamxbotz_fetch_media(
            limit * 10
        )

        grouped = defaultdict(list)

        series_pattern = re.compile(
            r"^(.*?)(?:"
            r"S(\d{1,2})"
            r"|Season\s*(\d{1,2})"
            r")"
            r"(?:"
            r"\s*E(\d{1,3})"
            r"|\s*Episode\s*(\d{1,3})"
            r")?"
            r"(?:\s*Combined)?\b",
            re.IGNORECASE,
        )

        for file in cursor:
            file_name = getattr(
                file,
                "file_name",
                "",
            )

            if not file_name:
                continue

            match = series_pattern.search(
                file_name
            )

            if not match:
                continue

            title_part = match.group(1).strip()

            season_value = (
                match.group(2)
                or match.group(3)
            )

            if not season_value:
                continue

            season = int(season_value)

            title = await dreamxbotz_clean_title(
                title_part,
                is_series=False,
            )

            if not title:
                continue

            grouped[title].append(season)

        return {
            title: sorted(set(seasons))[:10]
            for title, seasons in grouped.items()
            if seasons
        }

    except Exception:
        logger.exception(
            "Error getting series list"
        )
        return {}
