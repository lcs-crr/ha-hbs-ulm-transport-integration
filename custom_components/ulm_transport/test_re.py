import re
from datetime import datetime

time_str = "2023-10-19T13:27:00+02:00"
dt = datetime.strptime(time_str, "%H:%M")
print(dt)