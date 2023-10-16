from cmsplugin_lotus.models import (
    PRIVATE_ONLY,
    PUBLIC_AND_PRIVATE,
    PUBLIC_ONLY,
)
from lotus.models import Article


def _set_privacy_filter_anonymous(article_filter, privacy_criterion):
    """
    Set privacy filters for anonymous users.

    This function takes an article filter and a privacy criterion,
    and applies the privacy settings suitable for anonymous users.

    Args:
        article_filter (ArticleQuerySetMaker): The initial article filter.
        privacy_criterion (str): The privacy settings criterion.

    Returns:
        ArticleQuerySetMaker: The updated ArticleQuerySetMaker object with applied
        filters.
    """
    if privacy_criterion == PRIVATE_ONLY[0][0]:
        return Article.objects.none
    if privacy_criterion in [PUBLIC_ONLY[0][0], PUBLIC_AND_PRIVATE[0][0]]:
        article_filter.public_only = True
        article_filter.private_only = False
    return article_filter


def _set_privacy_filter_logged_user(article_filter, privacy_criterion):
    """
    Set privacy filters for logged-in users.

    This function takes an article filter and a privacy criterion,
    and applies the privacy settings suitable for logged-in users.

    Args:
        article_filter (ArticleQuerySetMaker): The initial article filter.
        privacy_criterion (str): The privacy settings criterion.

    Returns:
        ArticleQuerySetMaker: The updated ArticleQuerySetMaker object with applied
        filters.
    """
    if privacy_criterion == PUBLIC_ONLY[0][0]:
        article_filter.public_only = True
        article_filter.private_only = False
    elif privacy_criterion == PRIVATE_ONLY[0][0]:
        article_filter.private_only = True
        article_filter.public_only = False
    elif privacy_criterion == PUBLIC_AND_PRIVATE[0][0]:
        article_filter.private_only = None
        article_filter.public_only = None
    return article_filter


def apply_privacy_filter(instance, request, article_filter):
    """
    Apply privacy filters based on user authentication status.

    This function checks if the user is anonymous or logged in and applies the
    appropriate privacy filters to the article filter.

    Args:
        instance (ArticlePluginParams): An instance of the plugin parameters.
        request (HTTPRequest): The current HTTP request.
        article_filter (ArticleQuerySetMaker): The initial article filter.

    Returns:
        ArticleQuerySetMaker: The updated ArticleQuerySetMaker object with applied
        privacy filters.
    """
    privacy_criterion = instance.privacy_criterion
    if request.user.is_anonymous:
        article_filter = _set_privacy_filter_anonymous(
            article_filter,
            privacy_criterion
        )
    else:
        article_filter = _set_privacy_filter_logged_user(
            article_filter,
            privacy_criterion
        )
    return article_filter
