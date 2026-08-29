from store import save_feedback, _FEEDBACK


def test_save_feedback_appends():
    save_feedback("hello")
    assert "hello" in _FEEDBACK
