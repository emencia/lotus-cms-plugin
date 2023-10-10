from django.utils import timezone

from lotus.models import Article, Category
from taggit.models import Tag


class ArticleQuerySetMaker:
    """
    Create a Article queryset for filtering instances of Articles for
    LatestArticlesPlugin.

    This class takes various filtering parameters and provides methods to generate
    a filtered queryset based on these parameters.
    """

    def __init__(
        self,
        categories=Category.objects.none(),
        status=None,
        public_only=None,
        private_only=None,
        limit=None,
        featured=None,
        tags=Tag.objects.none()
    ):
        """
        Initialize a ArticleQuerySetMaker instance.

        Args:
            categories (BaseManager[Category], optional): Categories to filter by.
             Defaults to none.
            status (int, optional): Status to filter by. Defaults to None.
            public_only (bool, optional): Filter by public articles only.
             Defaults to None.
            private_only (bool, optional): Filter by private articles only.
             Defaults to None.
            limit (int, optional): Maximum number of articles to return.
             Defaults to None.
            featured (bool, optional): Filter by featured articles only.
             Defaults to None.
            tags (BaseManager[Tag], optional): Tags to filter by. Defaults to none.
        """
        self.categories = categories
        self.status = status
        self.private_only = private_only
        self.public_only = public_only
        self.featured = featured
        self.tags = tags

        self.limit = limit

    @classmethod
    def from_plugin_params(cls, params):
        """
        Create a ArticleQuerySetMaker instance from plugin parameters.

        Args:
            params (ArticlePluginParams): The plugin parameters to initialize from.

        Returns:
            ArticleQuerySetMaker: A new ArticleQuerySetMaker instance.
        """

        return cls(
            limit=params.cards_quantity,
            categories=params.categories,
            status=params.status,
            featured=params.featured,
            tags=params.tags,
        )

    def __call__(
        self, *,
        limit=None,
        public_only=None,
        private_only=None,
    ):
        """
        Call the ArticleQuerySetMaker to filter `Article` queryset based on set
        parameters.

        Args:
            limit (int, optional): Maximum number of articles to return.
             Overrides initial setting.
            public_only (bool, optional): Filter by public articles only.
             Overrides initial setting.
            private_only (bool, optional): Filter by private articles only.
             Overrides initial setting.

        Returns:
            QuerySet: The filtered queryset of articles.
        """
        qs_articles = Article.objects.all().distinct()
        qs_articles = self.filter_by_feature(qs_articles)
        qs_articles = self.filter_by_categories(qs_articles)
        qs_articles = self.filter_by_tags(qs_articles)
        qs_articles = self.filter_by_status(qs_articles)
        qs_articles = self.filter_by_privacy(qs_articles)
        qs_articles = self.filter_by_date(qs_articles)
        return self.apply_limit(qs_articles, limit)

    def filter_by_feature(self, qs_articles):
        """
        Filter `Article` queryset by the 'featured' field.

        Args:
            qs_articles (QuerySet): The initial `Article` queryset to filter.

        Returns:
            QuerySet: The filtered `Article` queryset based on `Article.featured`.
        """
        if isinstance(self.featured, bool):
            return qs_articles.filter(featured=self.featured)
        return qs_articles

    def filter_by_categories(self, qs_articles):
        """
        Filter `Article` queryset by the 'categories' field.

        Args:
            qs_articles (QuerySet): The initial `Article` queryset to filter.

        Returns:
            QuerySet: The filtered `Article` queryset based on `Article.categories`.
        """
        if self.categories.all():
            return qs_articles.filter(categories__in=self.categories.all())
        return qs_articles

    def filter_by_tags(self, qs_articles):
        """
        Filter `Article` queryset by the 'tags' field.

        Args:
            qs_articles (QuerySet): The initial `Article` queryset to filter.

        Returns:
            QuerySet: The filtered `Article` queryset based on `Article.tags`.
        """
        if self.tags.all():
            return qs_articles.filter(tags__in=self.tags.all())
        return qs_articles

    def filter_by_status(self, qs_articles):
        """
        Filter `Article` queryset by the 'status' field.

        Args:
            qs_articles (QuerySet): The initial `Article` queryset to filter.

        Returns:
            QuerySet: The filtered `Article` queryset based on `Article.status`.
        """
        if self.status is not None:
            return qs_articles.filter(status=self.status)
        return qs_articles

    def filter_by_privacy(self, qs_articles):
        """
        Filter `Article` queryset by the 'private' field.

        Args:
            qs_articles (QuerySet): The initial `Article` queryset to filter.

        Returns:
            QuerySet: The filtered `Article` queryset based on `Article.private`.
        """
        if self.public_only and not self.private_only:
            return qs_articles.filter(private=False)
        elif self.private_only and not self.public_only:
            return qs_articles.filter(private=True)
        return qs_articles

    def filter_by_date(self, qs_articles):
        """
        Filter `Article` queryset by the `publish_date` and `publish_end` fields.

        Args:
            qs_articles (QuerySet): The initial `Article` queryset to filter.

        Returns:
            QuerySet: The filtered `Article` queryset based on `Article.publish_date`
            and `Article.publish_end`.
        """
        date_ref = timezone.now().date()
        return (
            qs_articles
            .exclude(publish_date__gt=date_ref)
            .exclude(publish_end__lt=date_ref)
        )

    def apply_limit(self, qs_articles, limit):
        """
        Apply a limit to the number of instances returned.

        This method takes an initial `Article` queryset and an optional limit,
        and returns a subset of `Article` queryset based on that limit.

        Args:
            instances (QuerySet): The initial `Article` queryset to limit.
            limit (int, optional): The maximum number of `Article` instances to return.

        Returns:
            QuerySet: The limited set of instances.
        """
        limit = self.limit or limit
        return qs_articles[:limit] if limit else qs_articles
