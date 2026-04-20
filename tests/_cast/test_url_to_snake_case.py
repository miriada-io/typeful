import pytest

from typeful import url_to_snake_case


@pytest.mark.parametrize(
    ["url", "expected"],
    [
        pytest.param("http://google.com", "http_google_com"),
        pytest.param("https://example.com/path", "https_example_com_path"),
        pytest.param("https://dev.example.org/admin/", "https_dev_example_org_admin"),
    ],
)
def test_url_to_snake_case(url: str, expected: str) -> None:
    assert url_to_snake_case(url) == expected
