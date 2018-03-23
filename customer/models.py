from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
        Customer model for handling customers using our website.

        Arguments:
            user: one-to-one field appended to default User table.
            tel: mandatory telephone number.
            address: mandatory customer address.
            wechat: optional wechat.
            weibo: optional weibo.
            qq: optional qq.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # tel, address and zipcode are mandatory fields
    tel = models.CharField(default='unknown', max_length=50)
    address = models.CharField(default='unknown', max_length=50)
    # below are optional fields
    wechat = models.CharField(blank=True, max_length=50)
    weibo = models.CharField(blank=True, max_length=50)
    qq = models.CharField(blank=True, max_length=50)

    class Meta:
        db_table = 'db_customer'

    def get_name(self):
        """
            Get customer name.

            Return:
                Customer full name if it exists, otherwise username.
        """
        name = self.user.first_name + ' ' + self.user.last_name
        if name is not ' ':
            return name
        return self.user.username

    def get_email(self):
        """ Get customer registered email. """
        return self.user.email
