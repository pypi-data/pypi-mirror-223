from typing import Any

from saffier.db.querysets.queryset import QuerySet


class Manager:
    """
    Base Manager for the Saffier Models.
    To create a custom manager, the best approach is to inherit from the ModelManager.

    Example:
        from saffier.managers import ModelManager
        from saffier.models import Model


        class MyCustomManager(ModelManager):
            ...


        class MyOtherManager(ModelManager):
            ...


        class MyModel(saffier.Model):
            query = MyCustomManager()
            active = MyOtherManager()

            ...
    """

    def __init__(self, model_class: Any = None):
        self.model_class = model_class

    def get_queryset(self) -> "QuerySet":
        """
        Returns the queryset object.
        """
        return QuerySet(self.model_class)

    def __getattr__(self, item: Any) -> Any:
        """
        Gets the attribute from the queryset and if it does not
        exist, then lookup in the model.
        """
        try:
            return getattr(self.get_queryset(), item)
        except AttributeError:
            return getattr(self.model_class, item)
