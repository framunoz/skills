#!/usr/bin/env python3
"""Shared schema validation for logbook entry types. stdlib only."""
import re

SENSITIVE_PATTERNS = [
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'-----BEGIN .{1,40} PRIVATE KEY-----'),
    re.compile(r'(?i)(?:token|key|secret)[^\n]{0,20}[A-Za-z0-9_\-]{40,}'),
    re.compile(r'[A-Za-z0-9_\-]{40,}(?:[^\n]{0,20}(?:token|key|secret))', re.IGNORECASE),
]


def _check_sensitive(text: str) -> list[str]:
    found = []
    for pat in SENSITIVE_PATTERNS:
        if pat.search(text):
            found.append(pat.pattern)
    return found


def _scan_values(payload: dict) -> list[str]:
    """Recursively scan all string values for sensitive patterns."""
    hits = []
    for v in payload.values():
        if isinstance(v, str):
            hits.extend(_check_sensitive(v))
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, str):
                    hits.extend(_check_sensitive(item))
        elif isinstance(v, dict):
            hits.extend(_scan_values(v))
    return hits


def validate_tests(payload: dict) -> tuple[bool, list[str]]:
    errors = []
    went_well = payload.get("went_well") or []
    went_wrong = payload.get("went_wrong") or []
    if not went_well and not went_wrong:
        errors.append("At least one of 'went_well' or 'went_wrong' must be non-empty.")
    if not payload.get("title"):
        errors.append("'title' is required.")
    return (len(errors) == 0, errors)


def validate_collaboration(payload: dict) -> tuple[bool, list[str]]:
    errors = []
    ai = payload.get("ai_contribution") or ""
    human = payload.get("human_contribution") or ""
    if not ai.strip() and not human.strip():
        errors.append("At least one of 'ai_contribution' or 'human_contribution' must be non-empty.")
    if not payload.get("title"):
        errors.append("'title' is required.")
    return (len(errors) == 0, errors)


def validate_free(payload: dict) -> tuple[bool, list[str]]:
    errors = []
    if not (payload.get("body") or "").strip():
        errors.append("'body' is required and must be non-empty.")
    if not payload.get("title"):
        errors.append("'title' is required.")
    return (len(errors) == 0, errors)


def validate_amendment(payload: dict, existing_ids: dict[int, str]) -> tuple[bool, list[str]]:
    """existing_ids: {id -> ulid} map of all entries in the logbook."""
    errors = []
    if not payload.get("title"):
        errors.append("'title' is required.")
    if not (payload.get("reason") or "").strip():
        errors.append("'reason' is required.")
    if not (payload.get("body") or "").strip():
        errors.append("'body' is required.")
    amends = payload.get("amends")
    if not amends or not isinstance(amends, dict):
        errors.append("'amends' object with 'id' and 'ulid' is required.")
    else:
        target_id = amends.get("id")
        target_ulid = amends.get("ulid")
        if target_id not in existing_ids:
            errors.append(f"amends.id {target_id!r} does not exist in this logbook.")
        elif existing_ids[target_id] != target_ulid:
            errors.append(f"amends.ulid {target_ulid!r} does not match entry #{target_id}.")
    return (len(errors) == 0, errors)


def scan_sensitive(payload: dict) -> list[str]:
    """Return list of matched sensitive pattern descriptions, empty if clean."""
    return _scan_values(payload)
