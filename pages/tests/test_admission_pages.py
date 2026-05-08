import pytest
from django.urls import reverse

from pages.admission_pages import ADMISSION_PAGE_LIST

pytestmark = pytest.mark.django_db


FORBIDDEN_PHRASES = [
    "무조건 합격",
    "100% 합격",
    "광주 1등",
    "최고의 학원",
    "합격 보장",
    "수상 보장",
    "단기간 완성",
]


def admission_url(page):
    if page.get("url_name"):
        return reverse(page["url_name"])
    return reverse("admission_page", kwargs={"slug": page["slug"]})


@pytest.mark.parametrize("page", ADMISSION_PAGE_LIST, ids=[page["slug"] for page in ADMISSION_PAGE_LIST])
def test_admission_pages_render_seo_content_and_links(client, page):
    response = client.get(admission_url(page))

    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert f"<title>{page['title']}</title>" in content
    assert f'<meta name="description" content="{page["meta_description"]}">' in content
    assert f"<h1>{page['h1']}</h1>" in content
    assert page["intro"] in content

    for link in ADMISSION_PAGE_LIST:
        assert admission_url(link) in content

    for phrase in FORBIDDEN_PHRASES:
        assert phrase not in content
