"""Small shared helpers for the Estfeed integration."""

from __future__ import annotations

import re
from typing import Any

# Energy Identification Codes are 16 characters: a 2-digit issuing office,
# an object-type letter, 12 code characters and a check character. Matching
# is case-insensitive because some systems echo EICs in lower case.
_EIC_RE = re.compile(r"\b\d{2}[A-Z][A-Z0-9-]{12}[A-Z0-9]\b", re.IGNORECASE)

MAX_ERROR_DETAIL_LENGTH = 200


def slugify(name: str) -> str:
    """Reduce a friendly name to the slug used in statistic/entity IDs.

    Shared by ``async_setup_entry`` and the config flow (which rejects
    names that would collide with an already-configured entry's slug).
    """
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "estfeed"


def mask_eic(eic: str) -> str:
    """Hide all but the last four characters of a metering point EIC."""
    return f"…{eic[-4:]}"


def mask_eics(text: str) -> str:
    """Mask every EIC-looking token in free text (error messages, payloads)."""
    return _EIC_RE.sub(lambda m: mask_eic(m.group(0)), text)


def error_detail(payload: Any) -> str:
    """Short, EIC-masked description of an API error body for logs and errors.

    Error bodies can be large HTML pages or echo request parameters; keeping
    them short and masked stops them from flooding logs or leaking meter IDs
    into diagnostics and bug reports.
    """
    text = mask_eics(" ".join(str(payload).split()))
    if len(text) > MAX_ERROR_DETAIL_LENGTH:
        return text[:MAX_ERROR_DETAIL_LENGTH] + "…"
    return text
