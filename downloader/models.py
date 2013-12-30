from django.db import models

class Search(models.Model):
	name = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)	
	result = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name + ' - ' + str(self.date)