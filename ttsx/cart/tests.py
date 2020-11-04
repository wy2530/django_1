from django.test import TestCase

# Create your tests here.
import datetime
res=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
print(res)