from django.db import models
from django.contrib.auth.models import User


class Supervisor(models.Model):
    """
        Supervisor model for handling supervisor administrating the website.

        Arguments:
            user: one-to-one field appended to default User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_supervisor'

    def get_name(self):
        """
            Get supervisor name.

            Return:
                Supervisor full name if it exists, otherwise username.
        """
        name = self.user.first_name + ' ' + self.user.last_name
        if name is not ' ':
            return name
        return self.user.username

    def get_email(self):
        """ Get supervisor registered email. """
        return self.user.email
