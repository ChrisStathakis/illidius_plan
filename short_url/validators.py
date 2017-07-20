from django.core.exceptions import ValidationError

def validate_min_length(value):

    if len(value) < 6 and value:
        raise ValidationError('Η λέξη %s έχει λιγότερα από 6 γράμματα' % value)


