from app.auth.password_reset import RESET_LIMIT_PER_HOUR, request_password_reset


def test_first_five_requests_succeed():
    email = "abundant@example.com"
    base = 1_000_000.0
    for i in range(RESET_LIMIT_PER_HOUR):
        result = request_password_reset(email, now=base + i)
        assert result["status"] == 200


def test_sixth_request_within_hour_is_rate_limited():
    email = "sixth@example.com"
    base = 2_000_000.0
    for i in range(RESET_LIMIT_PER_HOUR):
        request_password_reset(email, now=base + i)
    sixth = request_password_reset(email, now=base + RESET_LIMIT_PER_HOUR)
    assert sixth["status"] == 429


def test_rate_limited_response_matches_generic_success_message():
    email = "generic@example.com"
    base = 3_000_000.0
    for i in range(RESET_LIMIT_PER_HOUR):
        allowed = request_password_reset(email, now=base + i)
    limited = request_password_reset(email, now=base + RESET_LIMIT_PER_HOUR)
    assert limited["message"] == allowed["message"]


def test_attempts_older_than_an_hour_are_pruned():
    email = "later@example.com"
    base = 4_000_000.0
    for i in range(RESET_LIMIT_PER_HOUR):
        request_password_reset(email, now=base + i)
    # More than an hour after the first attempt -- the window has rolled
    # forward, so this request should succeed again.
    later = request_password_reset(email, now=base + 3601)
    assert later["status"] == 200
