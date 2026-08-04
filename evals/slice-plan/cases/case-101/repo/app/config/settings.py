import os
import json  # unused -- left over from a removed feature
import sys  # unused


class Settings:
    def __init__(self):
        self.debug = os.environ.get("APP_DEBUG", "false").lower() == "true"
        self.max_upload_mb = int(os.environ.get("APP_MAX_UPLOAD_MB", "10"))
        # self.legacy_feature_flag = os.environ.get("LEGACY_FEATURE_FLAG", "off")
        # ^ old flag, feature was removed in 2025, nothing reads this anymore


settings = Settings()
