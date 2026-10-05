"""Tests for shared helpers."""

from __future__ import annotations

from custom_components.estfeed.utils import (
    MAX_ERROR_DETAIL_LENGTH,
    error_detail,
    mask_eic,
    mask_eics,
    slugify,
)


def test_slugify():
    assert slugify("My Home!") == "my_home"
    assert slugify("!!!") == "estfeed"


def test_mask_eic_keeps_last_four_characters():
    assert mask_eic("38ZEE-00000001-A") == "…01-A"


def test_mask_eics_masks_every_eic_in_text():
    text = "meters 38ZEE-00000001-A and 38zee-00000002-b not authorised"
    masked = mask_eics(text)
    assert "38ZEE-00000001-A" not in masked
    assert "38zee-00000002-b" not in masked
    assert masked == "meters …01-A and …02-b not authorised"


def test_mask_eics_leaves_other_text_alone():
    text = "403: Forbidden (traceId=4bf92f3577b34da6a3ce929d0e0e4736)"
    assert mask_eics(text) == text


def test_error_detail_truncates_and_flattens_long_bodies():
    detail = error_detail("<html>\n" + "x" * 1000 + "\n</html>")
    assert "\n" not in detail
    assert len(detail) == MAX_ERROR_DETAIL_LENGTH + 1
    assert detail.endswith("…")


def test_error_detail_masks_eics_in_payloads():
    detail = error_detail({"message": "No access to 38ZEE-00000001-A"})
    assert "38ZEE-00000001-A" not in detail
    assert "…01-A" in detail
