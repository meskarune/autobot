#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that rolls a dice of variable sides"""

import random


def rollDie(sides):
    """Get a random number between 1 and N"""
    try:
        count = int(sides) + 1
        roll = random.randrange(1,count)
        return roll
    except ValueError:
        message = "I'm sorry, that isn't a valid number, please tell me the number of sides you want. dice <num>"
        return message
    except:
        return
