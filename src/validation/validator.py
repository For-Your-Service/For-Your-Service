class ValidationError(Exception):
    pass

def validate_veteran_profile(profile):
    if not profile or not isinstance(profile, dict):
        raise ValidationError('Invalid profile format')
    return True
