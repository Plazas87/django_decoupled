"""Template tags for dictionaries."""
from django import template

register = template.Library()


@register.filter
def macro_avg(mapping):
    """Return the support value from a classification report."""
    return mapping["macro avg"]


@register.filter
def weighted_avg(mapping):
    """Return the support value from a classification report."""
    return mapping["weighted avg"]


@register.filter
def support(mapping):
    """Return the support value from a classification report."""
    return mapping["support"]


@register.filter
def f1_score(mapping):
    """Return the f1-score value from a classification report."""
    return mapping["f1-score"]


@register.filter
def recall(mapping):
    """Return the recall value from a classification report."""
    return mapping["recall"]


@register.filter
def precision(mapping):
    """Return the precision value from a classification report."""
    return mapping["precision"]


@register.filter
def percentage(value):
    """Return the percentage of value."""
    return value * 100
