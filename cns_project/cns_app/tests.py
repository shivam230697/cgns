from django.test import TestCase


# Create your tests here.
class CnsTest(TestCase):
    def setUp(self):
        print("setup")
        lion = "Sher"

    def test_animal(self):
        self.assertEqual('sher', 'sher', 'not sher equals')
