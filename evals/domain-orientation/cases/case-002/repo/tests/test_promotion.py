from datetime import datetime, timedelta

import pytest

from deployment import Deployment
from promotion import PromotionDenied, promote


def test_promotion_denied_without_soak_time():
    dep = Deployment(id=1, artifact_id="a1", environment="dev", status="healthy",
                      started_at=datetime.utcnow().isoformat())
    with pytest.raises(PromotionDenied):
        promote(dep, approvals=[])


def test_promotion_denied_to_prod_without_approvals():
    dep = Deployment(id=2, artifact_id="a1", environment="staging", status="healthy",
                      started_at=(datetime.utcnow() - timedelta(hours=1)).isoformat())
    with pytest.raises(PromotionDenied, match="required-approvals"):
        promote(dep, approvals=[])
