import dht
import machine
import utime
import urequests
#sensor pin
dht_pin = 4
# api endpoint
api_url = "https://abungo.pythonanywhere.com/api"
#sensor read function
def read_dht_sensor():
    dht_sensor = dht.DHT11(machine.Pin(dht_pin))
    try:
        dht_sensor.measure()
        temperature_celsius = dht_sensor.temperature()
        humidity_percentage = dht_sensor.humidity()
        return temperature_celsius, humidity_percentage
    except Exception as e:
        print("Error reading DHT sensor:", e)
        return None, None

def post_data_to_api(temperature, humidity):
    # Current timestamp
    timestamp = utime.time()
    #adding 19800 to add 5.5hrs to the gmt time
    dt = utime.localtime(timestamp+19800)
    #formatting the string datetime
    str_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
    dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]
)
    #for debbuging
    print(str_time)
    
    data = {
        "timestamp": str_time,
        "temperature": temperature,
        "humidity": humidity
    }
    
    # Send POST request to the API endpoint
    try:
        response = urequests.post(api_url, json=data)
        print("API Response:", response.text)
    except Exception as e:
        print("Error posting data to API:", e)

while True:
    temperature, humidity = read_dht_sensor()

    if temperature is not None and humidity is not None:
        post_data_to_api(temperature, humidity)

    # Wait for some time before the next reading
    utime.sleep(300)  # Adjust the interval as needed