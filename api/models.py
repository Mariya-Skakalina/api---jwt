from django.db import models


# Create your models here.
class City(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class User(models.Model):
	login = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=100, blank=True, null=True)
	city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)


class Post(models.Model):
	name = models.CharField(max_length=255)
	body = models.TextField()
	price = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

