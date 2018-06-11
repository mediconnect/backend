# django
from django.db import models
from django.contrib.auth.models import User

# rest framework

# other

C2E = 0
E2C = 1


class Translator(models.Model):
    """
        Translator model for handling translator assisting the reservation.

        Arguments:
            user: one-to-one field appended to default User table.
            role: translator type
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(default = C2E)

    class Meta:
        db_table = 'db_translator'

    def get_name(self):
        """
            Get translator name.

            Return:
                Translator full name if it exists, otherwise username.
        """
        name = self.user.first_name + ' ' + self.user.last_name
        if name is not ' ':
            return name
        return self.user.username

    def get_email(self):
        """ Get translator registered email. """
        return self.user.email

    def get_role(self):
        """Get translator role"""
        return self.role