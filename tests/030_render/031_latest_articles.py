from lotus_cms_plugin.cms_plugins import LatestArticlesPlugin
from lotus_cms_plugin.factories.user import UserFactory
from lotus.choices import STATUS_DRAFT, STATUS_PUBLISHED
from lotus.factories import ArticleFactory, CategoryFactory
from lotus_cms_plugin.models import (
    PRIVATE_ONLY,
    PUBLIC_AND_PRIVATE,
    PUBLIC_ONLY,
)
from lotus_cms_plugin.utils.tests.cms_tests import CMSPluginTestCase
from lotus_cms_plugin.utils.tests.html_response import html_pyquery

from tests.utils import FixturesTestCaseMixin


class AnonymousTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    def setUp(self):
        self.category1 = CategoryFactory.create(title='Category 1', language='en')
        self.category2 = CategoryFactory.create(title='Category 2', language='fr')
        self.article1 = ArticleFactory.create(
            title='published and public',
            status=STATUS_PUBLISHED,
            private=False,
            language='en',
            fill_categories=[self.category1],
        )
        self.article2 = ArticleFactory.create(
            title='published and private',
            status=STATUS_PUBLISHED,
            private=True,
            language='fr',
            fill_categories=[self.category2]
        )
        self.article3 = ArticleFactory.create(
            title='unpublished and private',
            status=STATUS_DRAFT,
            private=True,
            language='fr',
            fill_categories=[self.category2]
        )
        self.article4 = ArticleFactory.create(
            title='unpublished and public',
            status=STATUS_DRAFT,
            private=True,
            language='fr',
            fill_categories=[self.category2]
        )

    def test_default(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 1
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' in displayed_title
        assert 'published and private' not in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title

    def test_private_only(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
            privacy_criterion=PRIVATE_ONLY[0][0],
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 0
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' not in displayed_title
        assert 'published and private' not in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title

    def test_public_only(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
            privacy_criterion=PUBLIC_ONLY[0][0],
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 1
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' in displayed_title
        assert 'published and private' not in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title

    def test_private_and_public_only(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
            privacy_criterion=PUBLIC_AND_PRIVATE[0][0],
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 1
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' in displayed_title
        assert 'published and private' not in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title


class LoggedInTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)
        self.category1 = CategoryFactory.create(title='Category 1', language='en')
        self.category2 = CategoryFactory.create(title='Category 2', language='fr')
        self.article1 = ArticleFactory.create(
            title='published and public',
            status=STATUS_PUBLISHED,
            private=False,
            language='en',
            fill_categories=[self.category1],
        )
        self.article2 = ArticleFactory.create(
            title='published and private',
            status=STATUS_PUBLISHED,
            private=True,
            language='fr',
            fill_categories=[self.category2]
        )
        self.article3 = ArticleFactory.create(
            title='unpublished and private',
            status=STATUS_DRAFT,
            private=True,
            language='fr',
            fill_categories=[self.category2]
        )
        self.article4 = ArticleFactory.create(
            title='unpublished and public',
            status=STATUS_DRAFT,
            private=True,
            language='fr',
            fill_categories=[self.category2]
        )

    def test_default(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 1
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' in displayed_title
        assert 'published and private' not in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title

    def test_private_only(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
            privacy_criterion=PRIVATE_ONLY[0][0],
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 1
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' not in displayed_title
        assert 'published and private' in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title

    def test_public_only(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
            privacy_criterion=PUBLIC_ONLY[0][0],
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 1
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' in displayed_title
        assert 'published and private' not in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title

    def test_private_and_public_only(self):
        placeholder, model_instance, context, html = self.create_basic_render(
            LatestArticlesPlugin,
            privacy_criterion=PUBLIC_AND_PRIVATE[0][0],
        )

        dom = html_pyquery(html)

        item_titles = dom.find(".card-title")
        assert len(item_titles) == 2
        displayed_title = [x.text for x in item_titles]

        assert 'published and public' in displayed_title
        assert 'published and private' in displayed_title
        assert 'unpublished and private' not in displayed_title
        assert 'unpublished and public' not in displayed_title
