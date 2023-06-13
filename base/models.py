from django.db import models

class State(models.Model):
    name=models.CharField(max_length=30)
    income_tax=models.IntegerField()
    tax_brackets=models.IntegerField()

    def __str__(self):
        return self.name



