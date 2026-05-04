"""
End-to-end smoke test with the ASR call mocked.

Why mocked: this sandbox's egress allowlist blocks YouTube media servers
and openaipublic.azureedge.net, so neither yt-dlp nor whisper.load_model
can run here. Both work normally in any unrestricted environment.

What this proves: given a transcript string from EITHER path (captions or
ASR), the rest of the pipeline (LangChain Document wrap, keyword scoring,
briefing rendering, JSON serialization) is correct.
"""
import json
from pathlib import Path
from unittest.mock import patch

import youtube_briefing as yb


FAKE_ASR_OUTPUT = (
    "Saudi Arabia announced today that the Public Investment Fund will allocate "
    "fifty billion dollars to NEOM and other Vision 2030 giga-projects in Riyadh. "
    "AI investments and Red Sea tourism are central to the plan."
)

FAKE_CAPTIONS_OUTPUT = (
    "Welcome to LEAP 2026 in Riyadh. Today we discuss AI infrastructure, "
    "investment in Saudi Arabia, and Vision 2030 milestones."
)

FAKE_METADATA_A = {
    "video_id": "VIDEO_AAA",
    "title": "PIF NEOM Funding Announcement",
    "channel": "Saudi News",
    "duration_sec": 320,
    "upload_date": "20260415",
}
FAKE_METADATA_B = {
    "video_id": "VIDEO_BBB",
    "title": "LEAP 2026 Keynote",
    "channel": "LEAP",
    "duration_sec": 1820,
    "upload_date": "20260301",
}


def run() -> None:
    briefs = []

    # Case A: simulate captions hit -> no ASR call
    with patch.object(yb, "fetch_metadata", return_value=FAKE_METADATA_A), \
         patch.object(yb, "fetch_captions", return_value=(FAKE_ASR_OUTPUT, "en")), \
         patch.object(yb, "transcribe_with_docling",
                      side_effect=AssertionError("ASR should NOT run when captions exist")):
        briefs.append(yb.process_video("https://youtube.com/watch?v=VIDEO_AAA"))

    # Case B: simulate captions disabled -> ASR fallback fires
    with patch.object(yb, "fetch_metadata", return_value=FAKE_METADATA_B), \
         patch.object(yb, "fetch_captions", return_value=None), \
         patch.object(yb, "download_audio", return_value=Path("/tmp/fake.wav")), \
         patch.object(yb, "transcribe_with_docling", return_value=FAKE_CAPTIONS_OUTPUT):
        briefs.append(yb.process_video("https://youtube.com/watch?v=VIDEO_BBB"))

    # Assertions
    assert briefs[0].transcript_source == "youtube_captions", briefs[0].transcript_source
    assert briefs[1].transcript_source == "docling_asr", briefs[1].transcript_source
    assert briefs[0].keywords_hit.get("Vision 2030") == 1
    assert briefs[0].keywords_hit.get("NEOM") == 1
    assert briefs[1].keywords_hit.get("Vision 2030") == 1

    # LangChain Document round-trip
    docs = [b.to_document() for b in briefs]
    for d in docs:
        assert d.page_content
        assert "transcript_source" in d.metadata
        assert "video_id" in d.metadata

    # Render + persist
    md = yb.render_briefing(briefs)
    Path("briefing.md").write_text(md)
    Path("briefs.json").write_text(
        json.dumps([b.__dict__ for b in briefs], indent=2, ensure_ascii=False)
    )

    print("ALL ASSERTIONS PASSED\n")
    print("Doc[0] metadata keys:", sorted(docs[0].metadata.keys()))
    print("Doc[1] metadata keys:", sorted(docs[1].metadata.keys()))
    print("\n" + "=" * 60)
    print(md)


if __name__ == "__main__":
    run()
