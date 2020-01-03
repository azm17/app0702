# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:41:56 2020

@author: azumi
"""

import my_function2_sql as my_func

user_name = 'azumi'
user_pass = 'mamiya'

print('get_user_dic():\n', 
      my_func.get_user_dic())

print('get_user_info():\n',
      my_func.get_user_info())

print('sql_ALLuser_profile():\n', 
      my_func.sql_ALLuser_profile(user_name, user_pass))

print('kakunin():')