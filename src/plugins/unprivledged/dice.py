#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that rolls a dice of variable sides"""

import random


def rollDie(sides):
    """Get a random number between 1 and N"""
    try:
        counts = [0] * sides
        roll = random.randint(1,sides)
        counts[roll - 1] += 1
        return counts
    except ValueError:
        message = "I'm sorry, that isn't a number, please tell me the number of sides you want. dice <num>"
        return message
    except:
        return
