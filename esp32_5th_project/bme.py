import machine
import utime
import urequests
import bme280_float as bme280
#sensor pin
dht_pin = 4
# api endpoint
api_url = "https://abungo.pythonanywhere.com/api"
#sensor read function
def read_bme_sensor():
    i2c = machine.I2C(0,sda=machine.Pin(21),scl=machine.Pin(22))
    bme = bme280.BME280(i2c=i2c)
    try:
        temperature_celsius,pressure_hpa,humidity_percentage = bme.read_compensated_data()
        return temperature_celsius, humidity_percentage,pressure_hpa
    except Exception as e:
        print("Error reading BME sensor:", e)
        return None, None, None

def post_data_to_api(temperature, humidity,pressure):
    # Current timestamp
    timestamp = utime.time()
    #adding 19800 to add 5.5hrs to the gmt time
    dt = utime.localtime(timestamp+19800)
    #formatting the string datetime
    str_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
    dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
    #for debbuging
    #print(str_time)
    
    data = {
        "timestamp": str_time,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure/100
    }
    
    # Send POST request to the API endpoint
    try:
        response = urequests.post(api_url, json=data)
        print("API Response:", response.text)
    except Exception as e:
        print("Error posting data to API:", e)
def run():
    temperature,humidity,pressure = read_bme_sensor()
    if temperature is None and humidity is None and pressure is None:
        temperature,humidity,pressure = read_bme_sensor()
    if temperature is not None and humidity is not None and pressure is not None:
        post_data_to_api(temperature, humidity,pressure)
        # Wait for some time before the next reading
        utime.sleep(5)  # Adjust the interval as needed