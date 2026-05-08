from __future__ import annotations

import sys
from pathlib import Path


def call_api(prompt, options, context):
    config = options.get("config", {})
    base_path = Path(config.get("basePath", ".")).resolve()
    repo_root = Path(config.get("repoRoot", "../.."))
    if not repo_root.is_absolute():
        repo_root = (base_path / repo_root).resolve()
    src_path = repo_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from rag_benchmark.promptfoo import call_promptfoo_provider

    return call_promptfoo_provider(prompt, options, context)
