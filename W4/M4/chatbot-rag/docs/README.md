# About This Knowledge Base

Place the documents you want the chatbot to answer questions about in this folder.

## Supported formats

| Extension | Format           |
|-----------|------------------|
| `.txt`    | Plain text       |
| `.md`     | Markdown         |
| `.pdf`    | PDF              |
| `.docx`   | Word document    |
| `.html`   | HTML page        |

Subdirectories are supported — the ingest script walks the entire tree.

## How to ingest

After adding your files, run:

```sh
uv run python scripts/ingest.py
```

To wipe the existing collection and start fresh:

```sh
uv run python scripts/ingest.py --clear
```

To point at a different folder:

```sh
uv run python scripts/ingest.py --docs /path/to/my/files
```
