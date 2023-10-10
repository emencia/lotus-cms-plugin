import pytest
from datetime import timedelta
from django.utils import timezone

from lotus.choices import STATUS_DRAFT, STATUS_PUBLISHED
from lotus.factories import ArticleFactory, CategoryFactory, TagFactory
from lotus.models import Article, Category
from taggit.models import Tag

from lotus_cms_plugin.queryset_maker import ArticleQuerySetMaker


STATUS_FAKE = 9999


class MockPluginParams:
    def __init__(
        self,
        cards_quantity=None,  # Default value as per your model
        categories=None,
        status=STATUS_PUBLISHED,  # Default status
        featured=False,  # Default value
        tags=None,
    ):
        self.cards_quantity = cards_quantity
        self.categories = categories
        self.status = status
        self.featured = featured
        self.tags = tags


@pytest.fixture
def categories():
    category0 = CategoryFactory.create(title='Category 0', language='en')
    category1 = CategoryFactory.create(title='Category 1', language='fr')
    return [category0, category1]


@pytest.fixture
def tags():
    tag_0 = TagFactory.create(name="tag_0")
    tag_1 = TagFactory.create(name="tag_1")
    return [tag_0, tag_1]


@pytest.fixture
def articles(categories, tags):
    article1 = ArticleFactory.create(
        fill_categories=[categories[0]],
        fill_tags=[tags[0]],
        status=STATUS_PUBLISHED,
        private=False
    )
    article2 = ArticleFactory.create(
        fill_categories=[categories[1]],
        fill_tags=[tags[1]],
        status=STATUS_DRAFT,
        private=True
    )
    return [article1, article2]


def test_init_all_parameters_provided(db, categories, tags):
    qsm = ArticleQuerySetMaker(
        categories=categories,
        status="published",
        public_only=True,
        limit=10,
        featured=True,
        tags=tags
    )
    assert qsm.categories == categories
    assert qsm.status == "published"
    assert qsm.public_only is True
    assert qsm.limit == 10
    assert qsm.featured is True
    assert qsm.tags == tags


def test_init_no_parameters(db):
    qsm = ArticleQuerySetMaker()
    assert list(qsm.categories) == list(Category.objects.none())

    assert qsm.status is None
    assert qsm.public_only is None
    assert qsm.private_only is None
    assert qsm.limit is None
    assert qsm.featured is None
    assert list(qsm.tags) == list(Tag.objects.none())


def test_from_plugin_params_all_parameters(db, categories, tags):
    params = MockPluginParams(
        cards_quantity=10,
        categories=categories,
        status="published",
        featured=True,
        tags=tags
    )
    qsm = ArticleQuerySetMaker.from_plugin_params(params)

    assert qsm.limit == 10
    assert qsm.categories == categories
    assert qsm.status == "published"
    assert qsm.featured is True
    assert qsm.tags == tags


def test_from_plugin_params_partial_parameters(db, categories):
    params = MockPluginParams(categories=categories)
    qsm = ArticleQuerySetMaker.from_plugin_params(params)

    assert qsm.limit is None
    assert qsm.categories == categories
    assert qsm.status is STATUS_PUBLISHED
    assert qsm.featured is False
    assert qsm.tags is None


def test_call_all_instance_attributes_set(db, articles):
    qsm = ArticleQuerySetMaker(
        categories=Category.objects.filter(id__in=[articles[0].categories.first().id]),
        status=articles[0].status,
        limit=1
    )
    queryset = qsm()

    assert queryset.count() == 1
    assert queryset.first().title == articles[0].title


def test_call_partial_instance_attributes_set(db, articles):
    qsm = ArticleQuerySetMaker(status=articles[0].status)
    queryset = qsm()

    assert queryset.count() == 1
    assert queryset.first().title == articles[0].title


def test_call_no_instance_attributes_set(db, articles):
    qsm = ArticleQuerySetMaker()
    queryset = qsm()

    assert queryset.count() == len(articles)


def test_filter_by_feature_true(db, articles):
    ArticleFactory.create(featured=True)
    qsm = ArticleQuerySetMaker(featured=True)
    queryset = qsm.filter_by_feature(Article.objects.all())

    assert queryset.count() == 1
    assert queryset.first().featured is True


def test_filter_by_feature_false(db, articles):
    qsm = ArticleQuerySetMaker(featured=False)
    queryset = qsm.filter_by_feature(Article.objects.all())

    assert all(not article.featured for article in queryset)


def test_filter_by_feature_none(db, articles):
    qsm = ArticleQuerySetMaker()
    queryset = qsm.filter_by_feature(Article.objects.all())

    assert queryset.count() == len(articles)


def test_filter_by_categories_valid(db, categories, articles):
    qsm = ArticleQuerySetMaker(
        categories=Category.objects.filter(title__in=["Category 0"])
    )
    queryset = qsm.filter_by_categories(Article.objects.all())

    assert queryset.count() == 1


def test_filter_by_categories_none(db, articles):
    qsm = ArticleQuerySetMaker()
    queryset = qsm.filter_by_categories(Article.objects.all())

    assert queryset.count() == len(articles)


def test_filter_by_categories_invalid(db, articles):
    invalid_category = CategoryFactory.create(id=9999)
    # Assuming this ID doesn't exist in the test DB
    qsm = ArticleQuerySetMaker(
        categories=Category.objects.filter(id__in=[invalid_category.id])
    )
    queryset = qsm.filter_by_categories(Article.objects.all())

    assert queryset.count() == 0


def test_filter_by_tags_valid(db, tags, articles):
    qsm = ArticleQuerySetMaker(tags=Tag.objects.filter(name__in=["tag_0"]))
    queryset = qsm.filter_by_tags(Article.objects.all())

    assert queryset.count() == 1
    assert articles[0] in queryset


def test_filter_by_tags_none(db, articles):
    qsm = ArticleQuerySetMaker()
    queryset = qsm.filter_by_tags(Article.objects.all())

    assert queryset.count() == len(articles)


def test_filter_by_tags_invalid(db, articles):
    invalid_tag = TagFactory.create(id=9999)
    # Assuming this ID doesn't exist in the DB
    qsm = ArticleQuerySetMaker(tags=Tag.objects.filter(id__in=[invalid_tag.id]))
    queryset = qsm.filter_by_tags(Article.objects.all())

    assert queryset.count() == 0


def test_filter_by_status_valid(db, articles):
    qsm = ArticleQuerySetMaker(status=STATUS_PUBLISHED)
    queryset = qsm.filter_by_status(Article.objects.all())

    assert queryset.count() == 1
    assert all(article.status == STATUS_PUBLISHED for article in queryset)


def test_filter_by_status_none(db, articles):
    qsm = ArticleQuerySetMaker()
    queryset = qsm.filter_by_status(Article.objects.all())

    assert queryset.count() == len(articles)


def test_filter_by_status_invalid(db, articles):
    qsm = ArticleQuerySetMaker(status=STATUS_FAKE)
    queryset = qsm.filter_by_status(Article.objects.all())

    assert queryset.count() == 0


def test_filter_by_privacy_public_only(db, articles):
    qsm = ArticleQuerySetMaker(public_only=True)
    queryset = qsm.filter_by_privacy(Article.objects.all())

    assert queryset.count() == 1
    assert all(not article.private for article in queryset)


def test_filter_by_privacy_private_only(db, articles):
    qsm = ArticleQuerySetMaker(private_only=True)
    queryset = qsm.filter_by_privacy(Article.objects.all())

    assert queryset.count() == 1
    assert all(article.private for article in queryset)


def test_filter_by_privacy_both_flags_false(db, articles):
    qsm = ArticleQuerySetMaker(public_only=False, private_only=False)
    queryset = qsm.filter_by_privacy(Article.objects.all())

    assert queryset.count() == len(articles)


def test_filter_by_date_future_publish(db, articles):
    future_date = timezone.now() + timedelta(days=10)
    future_article = ArticleFactory.create(publish_date=future_date.date())
    qsm = ArticleQuerySetMaker()
    queryset = qsm.filter_by_date(Article.objects.all())

    assert future_article not in queryset


def test_filter_by_date_past_publish(db, articles):
    past_date = timezone.now() - timedelta(days=10)
    past_article = ArticleFactory.create(publish_date=past_date.date())
    qsm = ArticleQuerySetMaker()
    queryset = qsm.filter_by_date(Article.objects.all())

    assert past_article in queryset


def test_apply_limit_valid(db, articles):
    qsm = ArticleQuerySetMaker(limit=3)
    queryset = qsm.apply_limit(Article.objects.all(), None)
    assert queryset.count() == 2
