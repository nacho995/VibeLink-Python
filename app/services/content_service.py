import logging
from datetime import datetime, timezone
from urllib.parse import quote

import httpx

from app.core.config import get_settings
from app.schemas.content import ContentItemResponse, ContentDiscoveryResponse

logger = logging.getLogger(__name__)
settings = get_settings()

# TMDB Config
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# IGDB Config
IGDB_BASE_URL = "https://api.igdb.com/v4"
IGDB_IMAGE_BASE_URL = "https://images.igdb.com/igdb/image/upload/t_cover_big/"

# Twitch token cache
_twitch_access_token: str | None = None
_twitch_token_expiry: datetime = datetime.min


# ==================== MOVIES (TMDB) ====================


async def get_popular_movies(page: int = 1) -> list[ContentItemResponse]:
    try:
        url = f"{TMDB_BASE_URL}/movie/popular?api_key={settings.tmdb_api_key}&language=es-ES&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                logger.warning(f"TMDB API error: {response.status_code}")
                return []

            data = response.json()
            results = data.get("results", [])
            return [
                ContentItemResponse(
                    external_id=f"tmdb-movie-{m['id']}",
                    title=m.get("title") or m.get("name") or "Sin titulo",
                    type="Movie",
                    image_url=f"{TMDB_IMAGE_BASE_URL}{m['poster_path']}" if m.get("poster_path") else None,
                    backdrop_url=f"{TMDB_IMAGE_BASE_URL}{m['backdrop_path']}" if m.get("backdrop_path") else None,
                    description=m.get("overview", ""),
                    rating=m.get("vote_average", 0),
                    year=_parse_year(m.get("release_date") or m.get("first_air_date")),
                    genres=[],
                )
                for m in results
            ]
    except Exception as e:
        logger.error(f"Error fetching popular movies: {e}")
        return []


async def get_popular_series(page: int = 1) -> list[ContentItemResponse]:
    try:
        url = f"{TMDB_BASE_URL}/tv/popular?api_key={settings.tmdb_api_key}&language=es-ES&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                return []

            data = response.json()
            results = data.get("results", [])
            return [
                ContentItemResponse(
                    external_id=f"tmdb-tv-{m['id']}",
                    title=m.get("name") or m.get("title") or "Sin titulo",
                    type="Series",
                    image_url=f"{TMDB_IMAGE_BASE_URL}{m['poster_path']}" if m.get("poster_path") else None,
                    backdrop_url=f"{TMDB_IMAGE_BASE_URL}{m['backdrop_path']}" if m.get("backdrop_path") else None,
                    description=m.get("overview", ""),
                    rating=m.get("vote_average", 0),
                    year=_parse_year(m.get("first_air_date") or m.get("release_date")),
                    genres=[],
                )
                for m in results
            ]
    except Exception as e:
        logger.error(f"Error fetching popular series: {e}")
        return []


async def search_movies_and_series(query: str, page: int = 1) -> list[ContentItemResponse]:
    try:
        url = f"{TMDB_BASE_URL}/search/multi?api_key={settings.tmdb_api_key}&language=es-ES&query={quote(query)}&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                return []

            data = response.json()
            results = data.get("results", [])
            items = []
            for m in results:
                media_type = m.get("media_type")
                if media_type not in ("movie", "tv"):
                    continue
                items.append(
                    ContentItemResponse(
                        external_id=f"tmdb-{media_type}-{m['id']}",
                        title=m.get("title") or m.get("name") or "Sin titulo",
                        type="Movie" if media_type == "movie" else "Series",
                        image_url=f"{TMDB_IMAGE_BASE_URL}{m['poster_path']}" if m.get("poster_path") else None,
                        backdrop_url=f"{TMDB_IMAGE_BASE_URL}{m['backdrop_path']}" if m.get("backdrop_path") else None,
                        description=m.get("overview", ""),
                        rating=m.get("vote_average", 0),
                        year=_parse_year(m.get("release_date") or m.get("first_air_date")),
                        genres=[],
                    )
                )
            return items
    except Exception as e:
        logger.error(f"Error searching movies/series: {e}")
        return []


# ==================== GAMES (IGDB via Twitch) ====================


async def _get_twitch_token() -> str | None:
    global _twitch_access_token, _twitch_token_expiry

    if _twitch_access_token and datetime.now(timezone.utc) < _twitch_token_expiry.replace(tzinfo=timezone.utc) if _twitch_token_expiry.tzinfo is None else _twitch_token_expiry:
        return _twitch_access_token

    try:
        url = f"https://id.twitch.tv/oauth2/token?client_id={settings.twitch_client_id}&client_secret={settings.twitch_client_secret}&grant_type=client_credentials"
        async with httpx.AsyncClient() as client:
            response = await client.post(url)
            if response.status_code != 200:
                logger.warning(f"Twitch OAuth error: {response.status_code}")
                return None

            data = response.json()
            _twitch_access_token = data.get("access_token")
            expires_in = data.get("expires_in", 0)
            _twitch_token_expiry = datetime.now(timezone.utc).replace(tzinfo=None).__class__.now(timezone.utc)
            from datetime import timedelta
            _twitch_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)
            return _twitch_access_token
    except Exception as e:
        logger.error(f"Error getting Twitch token: {e}")
        return None


async def _igdb_query(endpoint: str, body: str) -> dict | list | None:
    token = await _get_twitch_token()
    if not token:
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{IGDB_BASE_URL}/{endpoint}",
                headers={
                    "Client-ID": settings.twitch_client_id,
                    "Authorization": f"Bearer {token}",
                },
                content=body,
            )
            if response.status_code != 200:
                logger.warning(f"IGDB API error on {endpoint}: {response.status_code}")
                return None

            return response.json()
    except Exception as e:
        logger.error(f"Error querying IGDB: {e}")
        return None


async def get_popular_games(page: int = 1) -> list[ContentItemResponse]:
    try:
        offset = (page - 1) * 20
        query = f"fields name,cover.image_id,rating,first_release_date,genres.name,platforms.name,summary; where rating > 70 & cover != null; sort rating desc; limit 20; offset {offset};"

        games = await _igdb_query("games", query)
        if not games or not isinstance(games, list):
            return []

        return [_igdb_game_to_content_item(g) for g in games]
    except Exception as e:
        logger.error(f"Error fetching popular games from IGDB: {e}")
        return []


async def search_games(query: str, page: int = 1) -> list[ContentItemResponse]:
    try:
        offset = (page - 1) * 20
        escaped_query = query.replace('"', '\\"')
        igdb_query = f'search "{escaped_query}"; fields name,cover.image_id,rating,first_release_date,genres.name,platforms.name,summary; where cover != null; limit 20; offset {offset};'

        games = await _igdb_query("games", igdb_query)
        if not games or not isinstance(games, list):
            return []

        return [_igdb_game_to_content_item(g) for g in games]
    except Exception as e:
        logger.error(f"Error searching games on IGDB: {e}")
        return []


# ==================== COMBINED ====================


async def get_discovery_content(page: int = 1) -> ContentDiscoveryResponse:
    import asyncio
    movies, series, games = await asyncio.gather(
        get_popular_movies(page),
        get_popular_series(page),
        get_popular_games(page),
    )
    return ContentDiscoveryResponse(movies=movies, series=series, games=games)


async def search_all(query: str, page: int = 1) -> list[ContentItemResponse]:
    import asyncio
    movies_series, games = await asyncio.gather(
        search_movies_and_series(query, page),
        search_games(query, page),
    )
    results = movies_series + games
    results.sort(key=lambda c: c.rating, reverse=True)
    return results


# ==================== HELPERS ====================


def _parse_year(date_str: str | None) -> int | None:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str[:10], "%Y-%m-%d").year
    except (ValueError, IndexError):
        return None


def _igdb_game_to_content_item(g: dict) -> ContentItemResponse:
    cover = g.get("cover", {}) or {}
    image_id = cover.get("image_id")
    rating_raw = g.get("rating", 0) or 0
    first_release = g.get("first_release_date")

    year = None
    if first_release:
        try:
            year = datetime.fromtimestamp(first_release, tz=timezone.utc).year
        except (ValueError, OSError):
            pass

    genres = [ge.get("name", "") for ge in (g.get("genres") or []) if ge.get("name")]
    platforms = [p.get("name", "") for p in (g.get("platforms") or []) if p.get("name")]

    return ContentItemResponse(
        external_id=f"igdb-{g['id']}",
        title=g.get("name") or "Sin titulo",
        type="Game",
        image_url=f"{IGDB_IMAGE_BASE_URL}{image_id}.jpg" if image_id else None,
        backdrop_url=f"https://images.igdb.com/igdb/image/upload/t_screenshot_big/{image_id}.jpg" if image_id else None,
        description=g.get("summary") or "",
        rating=rating_raw / 10.0,
        year=year,
        genres=genres,
        platforms=platforms if platforms else None,
    )
