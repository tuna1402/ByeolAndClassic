import pytest

pytestmark = pytest.mark.django_db


EXPECTED_ROBOTS = """User-agent: *
Disallow:

Sitemap: https://byeolclassica.pythonanywhere.com/sitemap.xml
"""

REQUIRED_SITEMAP_URLS = [
    "https://byeolclassica.pythonanywhere.com/",
    "https://byeolclassica.pythonanywhere.com/curriculum/",
    "https://byeolclassica.pythonanywhere.com/admission/yejung-piano/",
    "https://byeolclassica.pythonanywhere.com/admission/yego-piano/",
    "https://byeolclassica.pythonanywhere.com/admission/music-college-piano/",
    "https://byeolclassica.pythonanywhere.com/admission/graduate-piano/",
]


def test_robots_txt_is_plain_text_with_sitemap(client):
    response = client.get("/robots.txt")

    assert response.status_code == 200
    assert response["Content-Type"] == "text/plain; charset=utf-8"
    assert response.content.decode("utf-8") == EXPECTED_ROBOTS


def test_sitemap_xml_is_xml_and_includes_required_urls(client):
    response = client.get("/sitemap.xml")

    assert response.status_code == 200
    assert response["Content-Type"].startswith(("application/xml", "text/xml"))

    body = response.content.decode("utf-8")
    assert body.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert "<urlset" in body
    assert "<html" not in body.lower()
    for url in REQUIRED_SITEMAP_URLS:
        assert f"<loc>{url}</loc>" in body


@pytest.mark.parametrize(
    "path",
    [
        "/admission/yejung-piano/",
        "/admission/yego-piano/",
        "/admission/music-college-piano/",
        "/admission/graduate-piano/",
    ],
)
def test_sitemap_admission_urls_render(client, path):
    response = client.get(path)

    assert response.status_code == 200


def test_favicon_ico_is_available(client):
    response = client.get("/favicon.ico")

    assert response.status_code == 200
    assert response["Content-Type"] == "image/x-icon"
    assert b"".join(response.streaming_content)


def test_base_template_includes_favicon_links(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.content.decode("utf-8")
    assert '<link rel="icon" href="/static/favicon.ico" sizes="any">' in body
    assert (
        '<link rel="icon" type="image/png" sizes="48x48" '
        'href="/static/images/favicon/favicon-48x48.png">'
    ) in body
    assert (
        '<link rel="icon" type="image/png" sizes="96x96" '
        'href="/static/images/favicon/favicon-96x96.png">'
    ) in body
    assert (
        '<link rel="icon" type="image/png" sizes="192x192" '
        'href="/static/images/favicon/favicon-192x192.png">'
    ) in body
    assert (
        '<link rel="apple-touch-icon" sizes="180x180" '
        'href="/static/images/favicon/apple-touch-icon.png">'
    ) in body
