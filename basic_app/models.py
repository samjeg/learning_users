# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User)
	portfolio_site = models.URLField()
	# upload to folder in media folder
	picture = models.ImageField(upload_to='images')
