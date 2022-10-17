#A rule which add an extra %$ ammount to a Trip price.
#Temporal model: We receive a JSON from Backoffice admin web page
#and updates the rule here
from abc import ABC, abstractmethod
from datetime import *
from mimetypes import init
from pickle import NONE
from time import time
from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import Self


#Defining abstract method calculate_percent like an interface.
#Thus calculate_percent() must be implemented in all Rules.
class Rule(ABC):

    @abstractmethod
    def calculate_percent(self):
        pass
#RushHourRule implement Rule interface
class RushHourRule(Rule):
    rush_init: time
    rush_end: time
    percent_to_add_in_rush: float

    def __init__(self):
        self.percent_to_add_in_rush = 0
        self.rush_init = datetime.today().time().replace(0,0,0)
        self.rush_end = datetime.today().time().replace(23,59,59)

    def set_percent(self,new_percent: float):
        self.percent_to_add_in_rush = new_percent

    def set_init(self,new_init: time):
        self.rush_init = new_init

    def get_init(self):
        return self.rush_init

    def set_end(self,new_end: time):
        self.rush_end = new_end

    def get_end(self):
        return self.rush_end

    def calculate_percent(self):
        if (datetime.now().time() > self.rush_init) & (datetime.now().time() < self.rush_end):
            return self.percent_to_add_in_rush
        else:
            return 0

class DriverRule(Rule):
    day_percent: float
    monthly_percent: float
    old_percent: float

    def __init__(self):
        self.day_percent = 0
        self.monthly_percent = 0
        self.old_percent = 0

    def set_day_percent(self,percent: float):
        self.day_percent = percent

    def set_monthly_percent(self,percent: float):
        self.monthly_percent = percent

    def set_old_percent(self,percent: float):
        self.old_percent = percent    

    def calculate_percent(self):
        percent = 0
        for var in vars(self):
            percent += vars(self)[var]
        return percent

class BusinessRule(Rule):
    rules: List[Rule]

    def __init__(self):
        self.rules = list()

    def append_rule(self,a_rule: Rule):
        for rule in self.rules:
            if type(rule) == type(a_rule):
                self.rules.remove(rule)
                self.rules.append(a_rule)
                return None
        self.rules.append(a_rule)

    def calculate_percent(self):
        percent = 0
        for rule in self.rules:
            percent += rule.calculate_percent()
        return percent



a_rule = DriverRule()
a_rule.set_day_percent(5)
a_rule.set_monthly_percent(3)
print(a_rule.calculate_percent())
