#This file mainly exists to allow python setup.py test to work.
import unittest
from pypelibgui.models import RuleTableModel, RuleModel


class TestRules(unittest.TestCase):
    def test_creation(self):
        rt = RuleTableModel()
        rt.name = "tabla1"
        rt.type = "nonterminal"
        rt.save()
        
        r1 = RuleTableModel.objects.get(name="Tabla1")

        self.assertEquals(
            r1.inner.name,
            rtm.name,
            "Not properly creating Rule Tables")

    def test_deletion(self, ):
        RuleTableModel.objects.all().delete()
        rtm = RuleTableModel()
        rtm.name = "Tabla1"
        rtm.save()

        r1 = RuleTableModel.objects.get(name="Tabla1")

        r1.delete()

        self.asset
        r1 = RuleTableModel.objects.get(name="Tabla1")






def main():
    unittest.main()

if __name__ == "__main__":
    unittest.main()
