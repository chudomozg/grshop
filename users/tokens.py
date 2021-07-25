from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    # Token generator for activate user by email (email confirmation)
    # We will use username and timestamp to prevent decode username from token
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


user_activation_token = UserActivationTokenGenerator()