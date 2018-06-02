from django.template.defaultfilters import slugify
from django.core.exceptions import FieldError
import math


class SluggedModelMixin:
    """
    For use with Django models.
    Creates a slug from _slugify='title' and stores it in _slug_field='slug'.
    Overwrite these fields as needed.

    E.g.: 'Exercises to live by' --> 'exercises-to-live-by'
    E.g.:    'A great hamburger' --> 'a-great-hamburger'
    E.g.:    'A great hamburger' --> 'a-great-hamburger-2'
    """
    _slugify = 'title'
    _slug_field = 'slug'

    @staticmethod
    def __get_number_of_digits(n: int) -> int:
        return int(math.log10(n) + 1)

    def __ensure_fields_exists(self):
        error = "Field %(field)s does not exist on model " + self.__class__.__name__
        if not hasattr(self, self._slugify):
            raise FieldError(error % {'field': self._slugify})
        if not hasattr(self, self._slug_field):
            raise FieldError(error % {'field': self._slug_field})

    def _generate_unique_slug(self):
        self.__ensure_fields_exists()
        base = slugify(getattr(self, self._slugify))
        slug = base

        counter = 1
        max_length = self.__class__._meta.get_field(self._slug_field).max_length
        while self.__class__.objects.filter(**{self._slug_field: slug}):
            d = self.__get_number_of_digits(counter)
            s = base[0:max_length - (d + 1)].rstrip('-')

            slug = '%s-%s' % (s, counter)
            counter += 1

        setattr(self, self._slug_field, slug)

    def save(self, *args, **kwargs):
        if not getattr(self, self._slug_field, None):
            self._generate_unique_slug()
        super(SluggedMixin, self).save(*args, **kwargs)
