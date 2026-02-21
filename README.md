# AI Integration for Systematic Beat Making in FoxDot

A Gradio-based web application for browsing, editing, and executing [FoxDot](https://foxdot.org/) live-coding scripts. FoxDot scripts in the `data/` directory are listed in real time, and you can view and run them directly from the browser—making it easy to iterate on beat patterns, chord progressions, and song structures.

## Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** – Python package manager
- **[SuperCollider](https://supercollider.github.io/)** – audio synthesis engine
- **FoxDot Quark for SuperCollider**

### SuperCollider Setup

1. Install SuperCollider.
2. In SuperCollider, run:
   ```
   Quarks.install("FoxDot")
   ```
3. Go to **Language → Recompile Class Library**.
4. Run `FoxDot.start` in SuperCollider to boot the FoxDot server.

## Installation

```bash
uv sync
```

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_key_here
DATA_DIRECTORY=./data       # optional, defaults to ./data
```

## Usage

Start the Gradio web app:

```bash
uv run -m src.main
```

The app will launch in your browser. From there you can:

- **Browse** – The file list auto-refreshes every second, picking up any new or removed files in the data directory.
- **View** – Click a file to display its contents.
- **Run** – For `.py` files, click **▶ Run** to execute the script using the project's virtual environment Python.
- **Stop** – Click **⏹ Stop** to kill a running process.

## Project Structure

> Updated on 2026/02/22

```
├── src/
│   ├── main.py                 # Gradio app entry point
│   ├── components/
│   │   ├── schema.py           # Abstract Component base class
│   │   ├── home.py             # Root App component (layout + wiring)
│   │   ├── file_list.py        # File browser panel with live reload
│   │   └── file_content.py     # Code viewer + run/stop controls
│   ├── env/
│   │   └── __init__.py         # Environment config (dotenv)
│   ├── fs/
│   │   ├── writer.py           # FileSystem – read/write/list files
│   │   └── watcher.py          # FileSystemWatcher – watchdog observer
│   ├── process/
│   │   └── manager.py          # ProcessManager – subprocess run/stop
│   └── resources/
│       └── resources.py        # Resource registry for graceful cleanup
├── data/                       # FoxDot scripts (watched directory)
├── pyproject.toml
└── .env                        # API keys & config (not committed)
```
