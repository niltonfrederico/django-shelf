from django.db import models


class BaseCategorizedModel(models.Model):
    foo = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.foo


class Model1(BaseCategorizedModel):
    """Empty Model for testing purposes."""


class Model2(BaseCategorizedModel):
    """Empty Model for testing purposes."""


class Model3(BaseCategorizedModel):
    """Empty Model for testing purposes."""


class Model4(BaseCategorizedModel):
    """Empty Model for testing purposes."""


class Model5(BaseCategorizedModel):
    """Empty Model for testing purposes."""
