from src.config import endpoint_url, bucket, s3_bucket, prefix


def get_url_photos() -> list:
    expression = f"{endpoint_url}/{bucket}/{{key}}".format
    contents = s3_bucket.objects.filter(Prefix=prefix)
    return [expression(key=key.key) for key in contents if key.size]


def get_photos_in_media_format():
    mapping_attr: callable = lambda x: {'type': 'photo', 'media': x}
    return [mapping_attr(i) for i in get_url_photos()]