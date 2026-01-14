from news.utils import render_markdown_safe


def test_markdown_renders():
    rendered = render_markdown_safe("# Title\n\n**bold**")
    assert "<h1>" in rendered
    assert "<strong>" in rendered


def test_markdown_strips_script():
    rendered = render_markdown_safe("<script>alert(1)</script>hello")
    assert "script" not in rendered.lower()
    assert "hello" in rendered


def test_markdown_allows_links():
    rendered = render_markdown_safe("[link](https://example.com)")
    assert "<a" in rendered
    assert "https://example.com" in rendered
