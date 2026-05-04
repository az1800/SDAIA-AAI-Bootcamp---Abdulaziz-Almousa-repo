"""
M2.Ex4 Task 1: Vision 2030 Project Briefing Generator
=====================================================

Use case
--------
Riyadh-based analysts track Vision 2030 announcements (LEAP, NEOM, PIF, Misk,
SDAIA) that are published on YouTube. Many of these clips have captions, but
press conferences, panel sessions, and Arabic-only briefings often do not.

This pipeline ingests a list of YouTube URLs and produces a structured
briefing for each video, with a transcript-first / ASR-fallback strategy:

    1. Pull metadata via yt-dlp (LangChain YoutubeLoaderDL pattern).
    2. Try YouTube captions via youtube-transcript-api.
    3. If captions are absent, disabled, or unusable, download the audio
       with yt-dlp and run Docling's ASR pipeline.
    4. Wrap the result as a LangChain Document with rich metadata.
    5. Emit a markdown briefing.

The fallback is the non-trivial part: the same downstream extraction code
runs regardless of how the text was obtained.
"""

from __future__ import annotations

import json
import logging
import re
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import yt_dlp
from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

from docling.datamodel import asr_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import AsrPipelineOptions
from docling.document_converter import AudioFormatOption, DocumentConverter
from docling.pipeline.asr_pipeline import AsrPipeline


log = logging.getLogger("youtube_briefing")
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class VideoBrief:
    video_id: str
    url: str
    title: str
    channel: str
    duration_sec: int
    upload_date: str
    transcript_source: str          # "youtube_captions" | "docling_asr" | "failed"
    transcript_lang: str | None
    transcript: str
    keywords_hit: dict[str, int] = field(default_factory=dict)

    def to_document(self) -> Document:
        meta = {k: v for k, v in asdict(self).items() if k != "transcript"}
        return Document(page_content=self.transcript, metadata=meta)


# ---------------------------------------------------------------------------
# 1. Metadata via yt-dlp
# ---------------------------------------------------------------------------
_VIDEO_ID_RE = re.compile(
    r"(?:v=|\/shorts\/|youtu\.be\/|\/embed\/)([0-9A-Za-z_-]{11})"
)


def extract_video_id(url: str) -> str:
    m = _VIDEO_ID_RE.search(url)
    if not m:
        raise ValueError(f"Could not parse video id from {url}")
    return m.group(1)


def fetch_metadata(url: str) -> dict[str, Any]:
    opts = {"quiet": True, "skip_download": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "video_id": info.get("id"),
        "title": info.get("title", ""),
        "channel": info.get("uploader", ""),
        "duration_sec": int(info.get("duration") or 0),
        "upload_date": info.get("upload_date", ""),
    }


# ---------------------------------------------------------------------------
# 2. Captions path
# ---------------------------------------------------------------------------
PREFERRED_LANGS = ["en", "en-US", "en-GB", "ar", "ar-SA"]


def fetch_captions(video_id: str) -> tuple[str, str] | None:
    """Return (text, lang) if captions exist, else None."""
    try:
        api = YouTubeTranscriptApi()
        listing = api.list(video_id)
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return None
    except Exception as e:
        log.warning("caption listing failed for %s: %s", video_id, e)
        return None

    # Prefer manual over auto-generated, in our preferred language order.
    candidates = list(listing)
    candidates.sort(key=lambda t: (t.is_generated, PREFERRED_LANGS.index(t.language_code)
                                   if t.language_code in PREFERRED_LANGS else 99))
    if not candidates:
        return None

    chosen = candidates[0]
    try:
        fetched = chosen.fetch()
    except Exception as e:
        log.warning("caption fetch failed for %s: %s", video_id, e)
        return None

    text = " ".join(snippet.text for snippet in fetched).strip()
    if not text:
        return None
    return text, chosen.language_code


# ---------------------------------------------------------------------------
# 3. ASR fallback via Docling
# ---------------------------------------------------------------------------
def download_audio(url: str, out_dir: Path) -> Path:
    out_template = str(out_dir / "%(id)s.%(ext)s")
    opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "0",
        }],
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    return out_dir / f"{info['id']}.wav"


_asr_converter: DocumentConverter | None = None


def _get_asr_converter() -> DocumentConverter:
    """Build the Docling converter once. WHISPER_TINY keeps the demo fast."""
    global _asr_converter
    if _asr_converter is not None:
        return _asr_converter

    pipeline_options = AsrPipelineOptions()
    pipeline_options.asr_options = asr_model_specs.WHISPER_TINY

    _asr_converter = DocumentConverter(
        format_options={
            InputFormat.AUDIO: AudioFormatOption(
                pipeline_cls=AsrPipeline,
                pipeline_options=pipeline_options,
            )
        }
    )
    return _asr_converter


def transcribe_with_docling(audio_path: Path) -> str:
    converter = _get_asr_converter()
    result = converter.convert(audio_path)
    return result.document.export_to_markdown()


# ---------------------------------------------------------------------------
# 4. Orchestration
# ---------------------------------------------------------------------------
KEYWORDS = [
    "Vision 2030", "NEOM", "PIF", "giga-project", "Riyadh",
    "investment", "billion", "AI", "tourism", "Red Sea",
]


def score_keywords(text: str) -> dict[str, int]:
    lower = text.lower()
    return {k: lower.count(k.lower()) for k in KEYWORDS if lower.count(k.lower()) > 0}


def process_video(url: str, force_asr: bool = False) -> VideoBrief:
    log.info("processing %s", url)
    meta = fetch_metadata(url)
    video_id = meta["video_id"]

    transcript: str | None = None
    source: str = "failed"
    lang: str | None = None

    if not force_asr:
        cap = fetch_captions(video_id)
        if cap:
            transcript, lang = cap
            source = "youtube_captions"
            log.info("  captions found (%s, %d chars)", lang, len(transcript))

    if transcript is None:
        log.info("  no captions -> Docling ASR fallback")
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = download_audio(url, Path(tmp))
            transcript = transcribe_with_docling(audio_path)
        source = "docling_asr"
        lang = "auto"
        log.info("  ASR produced %d chars", len(transcript))

    return VideoBrief(
        video_id=video_id,
        url=url,
        title=meta["title"],
        channel=meta["channel"],
        duration_sec=meta["duration_sec"],
        upload_date=meta["upload_date"],
        transcript_source=source,
        transcript_lang=lang,
        transcript=transcript,
        keywords_hit=score_keywords(transcript),
    )


# ---------------------------------------------------------------------------
# 5. Briefing renderer
# ---------------------------------------------------------------------------
def render_briefing(briefs: list[VideoBrief]) -> str:
    lines = ["# Vision 2030 Video Briefing", ""]
    for b in briefs:
        lines += [
            f"## {b.title}",
            f"- Channel: {b.channel}",
            f"- Uploaded: {b.upload_date}  | Duration: {b.duration_sec}s",
            f"- Source: `{b.transcript_source}` ({b.transcript_lang})",
            f"- URL: {b.url}",
        ]
        if b.keywords_hit:
            kw = ", ".join(f"{k} ({n})" for k, n in sorted(
                b.keywords_hit.items(), key=lambda x: -x[1]))
            lines.append(f"- Keyword hits: {kw}")
        snippet = b.transcript.strip().replace("\n", " ")
        snippet = snippet[:400] + ("..." if len(snippet) > 400 else "")
        lines += ["", f"> {snippet}", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    # Two-video demo. The first has captions; the second is forced through
    # the ASR path to prove the fallback works end-to-end.
    demo_urls = [
        ("https://www.youtube.com/watch?v=jNQXAC9IVRw", False),  # "Me at the zoo"
        ("https://www.youtube.com/watch?v=jNQXAC9IVRw", True),   # forced ASR
    ]
    if len(sys.argv) > 1:
        demo_urls = [(u, False) for u in sys.argv[1:]]

    briefs: list[VideoBrief] = []
    for url, force in demo_urls:
        try:
            briefs.append(process_video(url, force_asr=force))
        except Exception as e:
            log.error("failed on %s: %s", url, e)

    out = render_briefing(briefs)
    Path("briefing.md").write_text(out)
    Path("briefs.json").write_text(
        json.dumps([asdict(b) for b in briefs], indent=2, ensure_ascii=False)
    )
    print(out)
