from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Permission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Role(models.Model):
    name = models.CharField(max_length=100)
    is_internal = models.BooleanField(default=False)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
    # 0 - ticket issuer, 1 - company admin, 2 - internal users, 3 - root user
    # access_level = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
