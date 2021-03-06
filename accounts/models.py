#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    
    USER_TASK_SEND_FUNDING = 'S'
    USER_TASK_RECEIVE_FUNDING = 'R'
    USER_TASK_DEFAULT = USER_TASK_SEND_FUNDING
    USER_TASK_CHOICES = (
        (USER_TASK_SEND_FUNDING, 'Send funding'), # send funding
        (USER_TASK_RECEIVE_FUNDING, 'Receive funding') # receive funding
    )
    GENDERCHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )


    gender = models.CharField(max_length=2, choices=GENDERCHOICES)
    date_of_birth = models.DateField("date of birth", blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name = "phone number", null=True, blank=True)
    following = models.ManyToManyField("self", through='Peer', symmetrical=False, related_name='followers')
    level = models.ForeignKey("Level", on_delete=models.SET_NULL, null=True)
    task = models.CharField(max_length=2, choices=USER_TASK_CHOICES, default=USER_TASK_DEFAULT)
    amount_sent = models.DecimalField("Amount sent", max_digits=8, decimal_places=2, default=0)
    amount_received = models.DecimalField("Amount received", max_digits=8, decimal_places=2, default=0)
    karma = models.FloatField(default=10)
    can_merge = models.BooleanField(default=False)

    def update_level(self, level=None):

        try:
            level_obj = Level.objects.get(order=level)
            self.level = level_obj.id
            self.save()
            return True

        except ObjectDoesNotExist:
            
            return False

    def up_lines(self):
        """
        Returns a list of query set containing user(s) to receive entry
        fee
        """
        return self.following.all()
    
    def down_lines(self):
        """
        Returns a list of query set containing user(s) to pay entry
        fee
        """
        return self.followers.all()

    def get_absolute_url(self):
        return reverse("user_profile", args=[self.username])

    
class Peer(models.Model):
    
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ('-created_at',)
        unique_together = (('user_from', 'user_to'),)

    def __str__(self):
        return '%(user_from)s ---->> %(user_to)s' % {'user_from':self.user_from, 'user_to':self.user_to}

class Level(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    order = models.PositiveSmallIntegerField()
    entry_fee = models.DecimalField("Entry fee", max_digits=8, decimal_places=2, help_text="Amount user must send to eligible user")
    level_reward = models.DecimalField("Level reward", max_digits=8, decimal_places=2, help_text="Amount users will receive")

    class Meta:
        verbose_name = "level"
        verbose_name_plural = "levels"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("level_detail", kwargs={"pk": self.pk})

class TransactionLog(models.Model):

    TRANSACTION_REJECTED = 'Rejected'
    TRANSACTION_PAID = 'Paid'
    TRANSACTION_IN_PROGRESS = 'In Progress'
    TRANSACTION_STATUS = (
        (TRANSACTION_IN_PROGRESS, TRANSACTION_IN_PROGRESS),
        (TRANSACTION_REJECTED, TRANSACTION_REJECTED),
        (TRANSACTION_PAID, TRANSACTION_PAID)
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS, default=TRANSACTION_IN_PROGRESS)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def update_status(self, new_status):

        self.status = new_status
        self.save()
            
    class Meta:
        verbose_name = "Transaction Log"
        verbose_name_plural = "Transaction Logs"

    def __str__(self):
        return '{} ---- {} ---- {}'.format(self.user, self.status, self.description)

    def get_absolute_url(self):
        return reverse("TransactionLog_detail", kwargs={"pk": self.pk})

class Remerge(models.Model):
    """
    keep tracts of users that needs to be re-merge 
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count = models.SmallIntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "re-merge"
        verbose_name_plural = "re-merging list"

    def __str__(self):
        return '{} on {} requires {} user(s)'.format(
            self.user, self.count, self.level
        )
