from machine import Pin, I2C
import ssd1306
import dht
import time

# Initialize I2C for OLED (SDA = 9, SCL = 8)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize DHT11 sensor (Data pin on GPIO 4)
sensor = dht.DHT11(Pin(4))

# Main loop for OLED display without interrupts
while True:
    try:
        # Measure temperature and humidity
        sensor.measure()
        temp = sensor.temperature()  # °C
        hum = sensor.humidity()       # %
        print(f"Temp = {temp}°C, Humidity = {hum}%")
        
        # Clear OLED display
        oled.fill(0)
        
        # Display text and values
        oled.text("DHT11 Sensor", 0, 0)
        oled.text(f"Temp: {temp} C", 0, 20)
        oled.text(f"Humidity: {hum}%", 0, 40)
        
        # Show on OLED
        oled.show()

        time.sleep(10)  # Blocking delay for 2 seconds

    except OSError as e:
        oled.fill(0)
        oled.text("Sensor Error", 0, 0)
        oled.show()
