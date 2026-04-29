from __future__ import annotations

import re

import bleach
import markdown

ALLOWED_TAGS = [
    "p",
    "br",
    "a",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "blockquote",
    "code",
    "pre",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "img",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title"],
    "th": ["colspan", "rowspan"],
    "td": ["colspan", "rowspan"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

LINK_REL = "noopener noreferrer"


def _ensure_link_rel(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attrs = match.group(1)
        if re.search(r"\srel\s*=", attrs, flags=re.IGNORECASE):
            attrs = re.sub(
                r"\srel\s*=\s*([\"'])(.*?)\1",
                f' rel="{LINK_REL}"',
                attrs,
                flags=re.IGNORECASE,
            )
        else:
            attrs = f"{attrs} rel=\"{LINK_REL}\""
        if not re.search(r"\starget\s*=", attrs, flags=re.IGNORECASE):
            attrs = f"{attrs} target=\"_blank\""
        return f"<a{attrs}>"

    return re.sub(r"<a([^>]*)>", repl, html, flags=re.IGNORECASE)


def render_markdown_safe(text: str) -> str:
    if not text:
        return ""

    rendered = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "nl2br"],
    )
    sanitized = bleach.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    return _ensure_link_rel(sanitized)
