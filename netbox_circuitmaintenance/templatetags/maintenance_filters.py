import re

import nh3
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = {
    "a",
    "b",
    "br",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "span",
    "strong",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "u",
    "ul",
}

ALLOWED_ATTRIBUTES = {
    "*": {"class", "style"},
    "a": {"href", "title", "target"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan", "scope"},
}

HTML_TAG_RE = re.compile(r"<[a-zA-Z][^>]*>")


def _looks_like_html(value):
    """Return True if the value appears to contain HTML markup."""
    return bool(HTML_TAG_RE.search(value))


@register.filter(name="sanitize_html")
def sanitize_html(value):
    """Sanitize HTML content, allowing safe formatting tags only.

    Plain-text content is escaped and has newlines converted to <br> tags.
    """
    if not value:
        return ""
    if _looks_like_html(value):
        return mark_safe(
            nh3.clean(
                value,
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                link_rel="noopener noreferrer nofollow",
            )
        )
    return mark_safe(escape(value).replace("\n", "<br>"))
