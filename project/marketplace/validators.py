from django.core.exceptions import ValidationError

def validate_score(score):
    if score > 5 or score < 1:
        raise ValidationError("Score is out of range!")
