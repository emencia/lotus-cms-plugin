from django.test import TransactionTestCase

from lotus.choices import STATUS_DRAFT, STATUS_PUBLISHED
from lotus.factories import ArticleFactory, CategoryFactory, TagFactory
from lotus.models import Article, Category
from taggit.models import Tag

from lotus_cms_plugin.cms_plugins import ArticleQuerySetMaker
from datetime import timedelta
from django.utils import timezone


class ArticleQuerySetMakerTest(TransactionTestCase):
    """
    This class contains test methods for various scenarios of ArticleQuerySetMaker.
    """
    def setUp(self):
        """
        Set up the test case by creating instances of Category, Tag, and Article.
        """
        self.category1 = CategoryFactory.create(title='Category 1', language='en')
        self.category2 = CategoryFactory.create(title='Category 2', language='fr')
        self.tag_1 = TagFactory.create()
        self.tag_2 = TagFactory.create()
        self.article1 = ArticleFactory.create(
            title='Test Article 1',
            status=STATUS_PUBLISHED,
            private=False,
            language='en',
            fill_categories=[self.category1],
        )
        self.article2 = ArticleFactory.create(
            title='Test Article 2',
            status=STATUS_DRAFT,
            private=True,
            language='fr',
            fill_categories=[self.category2]
        )
        self.article3 = ArticleFactory.create(
            title='Test Article 3',
            status=STATUS_PUBLISHED,
            private=True,
            language='en',
            fill_categories=[self.category1],
            fill_tags=[self.tag_1],
            featured=True
        )
        self.article4 = ArticleFactory.create(
            title='Test Article 4',
            status=STATUS_PUBLISHED,
            private=False,
            language='en',
            fill_categories=[self.category1],
            fill_tags=[self.tag_2],
        )

    def test_queryset_maker_private_only(self):
        """
        Test the ArticleQuerySetMaker with private_only=True.
        """
        queryset_maker = ArticleQuerySetMaker(private_only=True)
        queryset = queryset_maker()
        self.assertEqual(queryset.count(), 2)
        self.assertListEqual(list(queryset), [self.article3, self.article2])

    def test_queryset_maker_public_only(self):
        """
        Test the ArticleQuerySetMaker with public_only=True.
        """
        queryset_maker = ArticleQuerySetMaker(public_only=True)
        queryset = queryset_maker()
        self.assertEqual(queryset.count(), 2)
        self.assertListEqual(list(queryset), [self.article4, self.article1])

    def test_queryset_maker_limit(self):
        """
        Test the ArticleQuerySetMaker with a limit.
        """
        max_num_article = 3
        queryset_maker = ArticleQuerySetMaker(limit=max_num_article)
        queryset = queryset_maker()
        self.assertEqual(queryset.count(), max_num_article)
        excepted_queryset = (
            Article.objects
            .all()
            .order_by(*Article._meta.ordering)
            [:max_num_article]
        )
        self.assertListEqual(list(queryset), list(excepted_queryset))

    def test_queryset_maker_status(self):
        """
        Test the ArticleQuerySetMaker with STATUS_PUBLISHED and STATUS_DRAFT status.
        """
        queryset_maker = ArticleQuerySetMaker(status=STATUS_PUBLISHED)
        queryset = queryset_maker()
        self.assertEqual(queryset.count(), 3)
        self.assertListEqual(
            list(queryset),
            [self.article4, self.article3, self.article1]
        )

        queryset_maker_draft = ArticleQuerySetMaker(status=STATUS_DRAFT)
        queryset_draft = queryset_maker_draft()
        self.assertEqual(queryset_draft.count(), 1)
        self.assertEqual(queryset_draft.first(), self.article2)

    def test_queryset_maker_category(self):
        """
        Test the ArticleQuerySetMaker with specific categories.
        """
        queryset_maker = ArticleQuerySetMaker(
            categories=Category.objects.filter(title='Category 1')
        )
        queryset = queryset_maker()
        self.assertEqual(queryset.count(), 3)
        self.assertListEqual(
            list(queryset),
            [self.article4, self.article3, self.article1]
        )

        queryset_maker = ArticleQuerySetMaker(
            categories=Category.objects.filter(title='Category 2')
        )
        queryset = queryset_maker()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.article2)

    def test_queryset_maker_featured(self):
        """
        Test the ArticleQuerySetMaker with featured=True.
        """
        queryset_maker = ArticleQuerySetMaker(featured=True)

        queryset = queryset_maker()

        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.article3, queryset)

    def test_queryset_maker_tags(self):
        """
        Test the ArticleQuerySetMaker with specific tags.
        """
        queryset_maker = ArticleQuerySetMaker(
            tags=Tag.objects.filter(name__in=[self.tag_1.name, self.tag_2.name])
        )

        queryset = queryset_maker()

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.article3, queryset)
        self.assertIn(self.article4, queryset)

    def test_queryset_filter_publish_date(self):
        """
        ArticleQuerySetMaker with publish date filtering.

        Expected articles are included or excluded based on the publish date.
        """
        past_date = timezone.now() - timedelta(days=10)
        future_date = timezone.now() + timedelta(days=10)

        past_article = ArticleFactory.create(
            title='Past Article',
            publish_date=past_date.date()
        )
        futur_article = ArticleFactory.create(
            title='Future Article',
            publish_date=future_date.date()
        )
        unpublished_articles = ArticleFactory(
            title="unpublished",
            publish_end=past_date
        )
        queryset_maker = ArticleQuerySetMaker()
        queryset = queryset_maker()

        self.assertIn(past_article, queryset)
        self.assertNotIn(futur_article, queryset)
        self.assertNotIn(unpublished_articles, queryset)

    def test_queryset_maker_all_params(self):
        """
        Test the ArticleQuerySetMaker with all parameters.
        """
        queryset_maker = ArticleQuerySetMaker(
            status=STATUS_PUBLISHED,
            categories=Category.objects.filter(title__in=['Category 1']),
            private_only=True,
            limit=1,
            featured=True,
            tags=Tag.objects.filter(name=self.tag_1.name)
        )
        queryset = queryset_maker()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.article3)
