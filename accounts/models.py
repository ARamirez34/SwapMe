from django.db import models
from django.contrib.auth.models import User

# Extend User model with profile information
User.add_to_class('profile_pic', models.ImageField(upload_to='profile_pics/', blank=True, null=True))
User.add_to_class('bio', models.TextField(max_length=250, blank=True, default=''))
User.add_to_class('trades_completed', models.IntegerField(default=0))
