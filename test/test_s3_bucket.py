import pytest

from src.utils import get_photos_in_media_format, get_url_photos


@pytest.mark.skip("manual test")
def test_bucket_urls():
    assert get_url_photos(), 'Photos are included ? '


@pytest.mark.skip("manual test")
def test_mapping_media():
    assert get_photos_in_media_format(), 'Photos are included ? '
