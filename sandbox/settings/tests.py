"""
Django settings for tests
"""
from sandbox.settings.base import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Media directory dedicated to tests to avoid polluting other environment
# media directory
MEDIA_ROOT = VAR_PATH / "media-tests"  # noqa: F405

# Require sorl thumbnail to raise exception on errors to ensure tests fail
THUMBNAIL_DEBUG = True

# Available CMS page template for tests purposes only
TEST_PAGE_TEMPLATES = "pages/test.html"
CMS_TEMPLATES.append(  # noqa: F405
    (TEST_PAGE_TEMPLATES, "test-basic"),
)

BLOCKS_LOTUS_PLUGIN_TEMPLATES = [
    ("cmsplugin_lotus/latest_articles/default.html", "Default"),
]