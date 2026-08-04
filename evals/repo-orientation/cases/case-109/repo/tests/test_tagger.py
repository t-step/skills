from tagger import tag_image


def test_tag_image_returns_list():
    assert isinstance(tag_image("nonexistent.png"), list)
