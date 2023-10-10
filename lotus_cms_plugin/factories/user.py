import factory

from django.contrib.auth.hashers import make_password

from lotus_cms_plugin.utils.user import safe_get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    """
    Create a fake user with Faker.
    """

    class Meta:
        model = safe_get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = make_password("password")
