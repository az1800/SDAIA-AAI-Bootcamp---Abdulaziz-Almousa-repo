# M2.Ex4 Task 1: YouTube + Docling ASR Fallback

Vision 2030 Project Briefing Generator. Ingests YouTube URLs, fetches captions, falls back to Docling ASR when captions are unavailable, emits a structured briefing.

## Files

- `youtube_briefing.py`: pipeline module
- `M2_Ex4.qmd`: Quarto write-up
- `test_pipeline_mocked.py`: verifies the data flow with the network calls mocked
- `test_asr_local.py`: runs Docling ASR on a local synthesized clip (requires Whisper checkpoint download)

## Setup

```bash
pip install yt-dlp youtube-transcript-api langchain langchain-community langchain-core docling openai-whisper
sudo apt install -y ffmpeg
```

## Run

```bash
# With your own URLs
python youtube_briefing.py "https://www.youtube.com/watch?v=URL1" "https://www.youtube.com/watch?v=URL2"

# Built-in demo (captions path + forced ASR path on the same video)
python youtube_briefing.py
```

Outputs:

- `briefing.md`: rendered briefing
- `briefs.json`: structured records with transcripts and metadata

## Verify without network

```bash
python test_pipeline_mocked.py
```

Confirms that captions hits skip ASR, captions misses trigger ASR, and the LangChain `Document` wrapping plus keyword scoring work on both paths.

## Sandbox limitations encountered during development

Two network endpoints needed at runtime are not on the sandbox egress allowlist, so the live demo cannot be executed here:

- `*.googlevideo.com` for yt-dlp media download
- `openaipublic.azureedge.net` for the first-time Whisper checkpoint download

Both are reachable from any unrestricted machine, including a typical laptop or Colab.

## Design notes

- Captions fetcher uses `youtube-transcript-api` 1.x API: `YouTubeTranscriptApi().list(video_id)`, then prefers manual transcripts over auto-generated, and English/Arabic over other languages.
- ASR uses `docling.pipeline.asr_pipeline.AsrPipeline` with `WHISPER_TINY` for the demo. Swap to `WHISPER_TURBO` or `WHISPER_LARGE` in `_get_asr_converter()` for production.
- Output is a LangChain `Document`, so briefs slot into any retriever or summarization chain without further glue.
- Provenance: every record carries `transcript_source` (`youtube_captions` | `docling_asr`) so downstream consumers can apply different confidence levels to ASR text.
