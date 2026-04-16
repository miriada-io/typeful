import pytest

from type_cast import url_to_snake_case


@pytest.mark.parametrize(['url', 'expected'], [
    pytest.param('http://ya.ru', 'http_ya_ru'),
    pytest.param('https://example.com/path', 'https_example_com_path'),
    pytest.param('https://dev.example.org/admin/', 'https_dev_example_org_admin'),
])
def test_url_to_snake_case(url: str, expected: str) -> None:
    assert url_to_snake_case(url) == expected
