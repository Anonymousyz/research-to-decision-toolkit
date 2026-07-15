"""Backward-compatible reporting import for r2d.

The canonical Markdown renderer lives in :mod:`r2d.scoring` so the CLI and
library callers cannot drift to different report schemas.
"""
from .scoring import render_markdown

__all__ = ["render_markdown"]
