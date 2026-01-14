import pytest
from django.urls import reverse

from pages.models import PageContent, PageKey


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_name",
    [
        "greeting",
        "profile",
        "awards",
        "curriculum",
        "accompanist",
        "soloist",
        "masterclass",
    ],
)
def test_pages_render_without_content(client, url_name):
    response = client.get(reverse(url_name))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "key,url_name,title",
    [
        (PageKey.GREETING, "greeting", "인삿말 테스트"),
        (PageKey.PROFILE, "profile", "프로필 테스트"),
        (PageKey.AWARDS, "awards", "수상내역 테스트"),
        (PageKey.CURRICULUM, "curriculum", "커리큘럼 테스트"),
        (PageKey.ACCOMPANIST, "accompanist", "반주자 테스트"),
        (PageKey.SOLOIST, "soloist", "솔리스트 테스트"),
        (PageKey.MASTERCLASS, "masterclass", "마스터 클래스 테스트"),
    ],
)
def test_pages_render_with_content(client, key, url_name, title):
    PageContent.objects.update_or_create(
        key=key, defaults={"title": title, "content": "테스트 내용"}
    )

    response = client.get(reverse(url_name))

    assert response.status_code == 200
    assert title in response.content.decode("utf-8")
