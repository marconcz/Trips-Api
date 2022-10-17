# import tested class
from .price_rules import *

# test_with_unittest.py

from unittest import TestCase

class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    # def test_always_fails(self):
    #     self.assertTrue(False)

#Testint hour rule:
class rush_hour_testing(TestCase):
    def test_simple_rule(self):
        a_rush_rule = RushHourRule()
        assert a_rush_rule.calculate_percent() == 0
#Testint hour rule with custom percent setted:
    def test_custom_percent(self):
        a_rush_rule = RushHourRule()
        a_rush_rule.set_percent(5)
        assert a_rush_rule.calculate_percent() == 5
#Testint hour rule with custom init hour:
    def test_custom_init(self):
        a_rush_rule = RushHourRule()
        a_rush_rule.set_init(datetime.today().time().replace(8,0,0,0))
        assert  a_rush_rule.get_init() == datetime.today().time().replace(8,0,0,0)
#Testint hour rule with custom end hour:
    def test_custom_end(self):
        a_rush_rule = RushHourRule()
        a_rush_rule.set_end(datetime.today().time().replace(8,0,0,0))
        assert  a_rush_rule.get_end() == datetime.today().time().replace(8,0,0,0) 
#Testint hour rule with custom init and end, returning percentage setted between hours:
    def test_custom_rule_with_init_and_end(self):
        a_rush_rule = RushHourRule()
        a_rush_rule.set_init(datetime.today().time().replace(0,0,0,0))
        a_rush_rule.set_end(datetime.today().time().replace(23,59,59,0))
        a_rush_rule.set_percent(3)

        assert  a_rush_rule.calculate_percent() == 3
    
#Testint business rule:
class business_rule_testing(TestCase):
    def test_simple_business_rule(self):
        a_rule = BusinessRule()
        assert a_rule.calculate_percent() == 0
#Testing a simple business rule with a RushHourRule added:
    def test_simple_business_rule_with_rush(self):
        a_rule = BusinessRule()

        hour_rule = RushHourRule()
        hour_rule.set_percent(10)

        a_rule.append_rule(hour_rule)

        assert a_rule.calculate_percent() == 10
#Testing a simple business rule with 2 RushHourRule added
#If there is a previous RushHourRule, then the first rule is replaced with second
    def test_simple_business_rule_with_rush(self):
        a_rule = BusinessRule()

        hour_rule = RushHourRule()
        hour_rule.set_percent(10)

        other_hour_rule = RushHourRule()
        other_hour_rule.set_percent(8)

        a_rule.append_rule(hour_rule)
        a_rule.append_rule(other_hour_rule)

        assert a_rule.calculate_percent() == 8
#Testing a simple business rule with a RushHourRule and a DriverRule:
    def test_simple_business_rule_with_rush(self):
        a_rule = BusinessRule()

        hour_rule = RushHourRule()
        hour_rule.set_percent(10)

        a_driver_rule = DriverRule()
        a_driver_rule.set_day_percent(2)
        a_driver_rule.set_monthly_percent(5)

        a_rule.append_rule(hour_rule)
        a_rule.append_rule(a_driver_rule)

        assert a_rule.calculate_percent() == 17