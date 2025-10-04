import asyncio
from typing import Iterable, List

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.twitter import Tweet, search_tweets


def create_app() -> FastAPI:
    app = FastAPI(title="X Startup Idea Finder", version="0.1.0")

    templates = Jinja2Templates(directory="app/templates")

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index(
        request: Request,
        keywords: List[str] | None = Query(default=None, description="Keywords to search for"),
    ):
        combined_keywords: List[str] = _normalize_keywords(keywords)
        results: List[Tweet] = []
        query = ""
        error: str | None = None

        if combined_keywords:
            query = build_query(combined_keywords)
            try:
                results = await asyncio.to_thread(search_tweets, query)
            except Exception as exc:  # pragma: no cover - defensive fallback
                error = f"Unable to load posts: {exc}"

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "keywords": combined_keywords,
                "results": results,
                "query": query,
                "error": error,
            },
        )

    return app


def build_query(keywords: List[str]) -> str:
    base_phrases = ['"I\'d pay for"', '"Someone please build"']
    keyword_query = " ".join(
        f'"{keyword.strip()}"' if " " in keyword else keyword.strip()
        for keyword in keywords
        if keyword.strip()
    )
    phrases = " OR ".join(base_phrases)
    search_terms = f"({phrases})"
    if keyword_query:
        search_terms += f" {keyword_query}"
    filters = "-filter:links -filter:retweets -filter:replies"
    return f"{search_terms} {filters}".strip()


app = create_app()


def _normalize_keywords(keywords: Iterable[str] | None) -> List[str]:
    if not keywords:
        return []

    normalized: List[str] = []
    for keyword in keywords:
        if not keyword:
            continue
        parts = [part.strip() for part in keyword.split(",")]
        normalized.extend(part for part in parts if part)
    # Deduplicate while preserving order to keep the UX predictable
    seen: set[str] = set()
    deduped: List[str] = []
    for keyword in normalized:
        lowered = keyword.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(keyword)
    return deduped


if __name__ == "__main__":
    import os

    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=os.getenv("RELOAD", "0") == "1")
