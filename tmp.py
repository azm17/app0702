# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import my_function2_demo as my_func
import datetime

day_list=[]
data_list=[]
for i in range(31):
    day=datetime.date.today() - datetime.timedelta(days=i)
    strday=day.strftime("%Y-%m-%d")
    data=my_func.sql_data_per_day(strday)
    dassui_data=[(d['wa']-d['wb'])/d['wb'] for d in data]
    day_list.append(day.strftime("%m/%d"))
    if len(dassui_data)>0:
        data_list.append(sum(dassui_data) / len(dassui_data))
    else:
        data_list.append(-100)

data_list.reverse()
day_list.reverse()


plt.plot(data_list,'o')
plt.xticks(range(0,31)[::3],day_list[::3])

plt.grid(color='gray')
plt.ylim(-2,2)
plt.ylabel('Dehydration rate')
plt.xlabel('Date')
plt.title('Daily average')
