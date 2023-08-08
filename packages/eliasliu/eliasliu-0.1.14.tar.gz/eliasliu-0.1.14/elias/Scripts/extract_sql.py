# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:50:44 2023

@author: nlsm
"""

from elias import usual as u
from elias.missions.mission_assets import sql as s
# sql
sql = s.mysql.assets_039_dws_class_turnover_d_f()
u.extract_table_name_from_sql(sql)