from machine import Pin, I2C, Timer
import ssd1306
import dht
import time

# Initialize I2C for OLED (SDA = 9, SCL = 8)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize DHT11 sensor (Data pin on GPIO 4)
sensor = dht.DHT11(Pin(4))

# Global variables to store sensor readings
temp = 0
hum = 0

# Interrupt handler to read DHT11
def read_sensor(timer):
    global temp, hum
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"Interrupt: Temp = {temp}°C, Humidity = {hum}%")
    except OSError as e:
        print("Failed to read sensor")

# Set up a timer interrupt every 2 seconds
timer = Timer(0)
timer.init(period=2000, mode=Timer.PERIODIC, callback=read_sensor)

# Main loop for OLED display
while True:
    try:
        # Clear OLED display
        oled.fill(0)
        
        # Display text and values
        oled.text("DHT11 Sensor", 0, 0)
        oled.text(f"Temp: {temp} C", 0, 20)
        oled.text(f"Humidity: {hum}%", 0, 40)
        
        # Show on OLED
        oled.show()

        time.sleep(10)  # Small delay for display refresh

    except OSError as e:
        oled.fill(0)
        oled.text("Sensor Error", 0, 0)
        oled.show()
