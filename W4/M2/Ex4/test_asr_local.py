"""
Smoke test: runs the Docling ASR fallback against a local audio clip,
then exercises the keyword scorer and briefing renderer using the same
data structures the YouTube pipeline produces.

This proves the fallback pipeline works end-to-end without YouTube access.
"""
from pathlib import Path
from youtube_briefing import (
    transcribe_with_docling,
    score_keywords,
    render_briefing,
    VideoBrief,
)

AUDIO = Path("sample_16k.wav")

print("Running Docling ASR on local sample (this downloads Whisper-tiny on first run)...")
text = transcribe_with_docling(AUDIO)
print(f"\n--- ASR output ({len(text)} chars) ---\n{text}\n")

brief = VideoBrief(
    video_id="LOCAL_DEMO",
    url="file://sample_16k.wav",
    title="Synthetic Vision 2030 announcement (local demo)",
    channel="local",
    duration_sec=11,
    upload_date="20260504",
    transcript_source="docling_asr",
    transcript_lang="auto",
    transcript=text,
    keywords_hit=score_keywords(text),
)

print("Keyword hits:", brief.keywords_hit)
print("\nLangChain Document round-trip:")
doc = brief.to_document()
print("  metadata keys:", sorted(doc.metadata.keys()))
print("  page_content length:", len(doc.page_content))

briefing_md = render_briefing([brief])
Path("briefing_local.md").write_text(briefing_md)
print("\n--- Rendered briefing ---")
print(briefing_md)
