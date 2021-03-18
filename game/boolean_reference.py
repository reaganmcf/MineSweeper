#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For stepping debug feature, I need to be able to pass around a boolean so i need a wrapper object
# that way I can pass by reference not by value
class BooleanReference:
    def __init__(self, init_value: bool = False):
        self._val = init_value

    def set(self, new_value: bool):
        self._val = new_value
    
    def get(self):
        return self._val
