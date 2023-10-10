from django.forms import ValidationError
from django.test import TestCase

from lotus.choices import STATUS_PUBLISHED
from lotus.factories import CategoryFactory
from taggit.models import Tag
from lotus_cms_plugin.models import ArticlePluginParams


class TestArticlePluginParams(TestCase):
    def test_default_values(self):
        obj = ArticlePluginParams.objects.create()
        self.assertEqual(obj.title, "Articles")
        self.assertEqual(obj.cards_quantity, 5)
        self.assertEqual(obj.status, STATUS_PUBLISHED)
        self.assertEqual(obj.privacy_criterion, "public_only")
        self.assertEqual(obj.featured, False)

    def test_required_fields(self):
        with self.assertRaises(ValidationError):
            obj = ArticlePluginParams(title=None)
            obj.full_clean()

        with self.assertRaises(ValidationError):
            obj = ArticlePluginParams(cards_quantity=None)
            obj.full_clean()

    def test_copy_relations(self):
        obj1 = ArticlePluginParams.objects.create()
        obj2 = ArticlePluginParams.objects.create()

        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')
        category1 = CategoryFactory.create(title='cat1')
        category2 = CategoryFactory.create(title='cat2')

        obj1.tags.add(tag1, tag2)
        obj1.categories.add(category1, category2)

        obj2.copy_relations(obj1)

        self.assertListEqual(list(obj1.tags.all()), list(obj2.tags.all()))
        self.assertListEqual(list(obj1.categories.all()), list(obj2.categories.all()))
