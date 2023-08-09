from django.db import models


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        value = super(LowercaseEmailField, self).to_python(value)

        if isinstance(value, str):
            return value.lower()

        return value
    
    def from_db_value(self, data):
        value = super(LowercaseEmailField, self).from_db_value(value)

        if isinstance(value, str):
            return value.lower()

        return value   
