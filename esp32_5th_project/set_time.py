import machine
import urequests
import time

# Fetch the datetime string from the URL
response = urequests.get("https://abungo.pythonanywhere.com/get_time")
datetime_str = response.text
response.close()
# Parse the datetime string
year, month, day, hour, minute, second = map(int, datetime_str.split(' ')[0].split('-') + datetime_str.split(' ')[1].split(':'))
print(time.localtime())
# Set the RTC datetime
rtc = machine.RTC()
rtc.datetime((year, month, day, 0, hour, minute, second, 0))

# Retrieve and print the current time
current_time = rtc.datetime()
print("Current time:", current_time)