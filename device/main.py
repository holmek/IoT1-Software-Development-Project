import umqtt_robust2 as mqtt
from machine import UART
from time import sleep
from gps_bare_minimum import GPS_Minimum
from machine import I2C
from machine import Pin
from mpu6050 import MPU6050
import machine
from time import sleep
from machine import SoftI2C
import ssd1306
from machine import ADC

voltage_splitter = ADC(Pin(34))
voltage_splitter.atten(ADC.ATTN_11DB)

bzz = Pin(2, Pin.OUT, value=0)

i2c = I2C(0)
imu = MPU6050(i2c)

gps_port = 2
gps_speed = 9600

uart = UART(gps_port, gps_speed)
gps = GPS_Minimum(uart)

tackling_count = 0
battery_percentage = 0
tackling_count_value = 0
battery_percentage_value = 0
player_speed_data_gps_value = 0
status_indicator_on = 1

player_vibration_speed_completed_5 = False
player_vibration_speed_completed_10 = False
player_vibration_speed_completed_15 = False
player_vibration_speed_completed_20 = False

def player_oled_stats():
	i2c = SoftI2C(scl=Pin(33), sda=Pin(32))
	
	oled_width = 128
	oled_height = 64
	player_oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
	
	player_oled.text('BATTERI', 0, 0)
	player_oled.text(str(battery_percentage) + "%", 0, 10)
	player_oled.text('TACKLINGER', 0,22)
	player_oled.text(str(tackling_count), 0, 33)
	player_oled.text('SPEED', 0,45)
	player_oled.text(str(int(gps.get_speed())) + " kmt/t", 0, 55)
	player_oled.show()
	
def player_oled_startup():
	i2c = SoftI2C(scl=Pin(33), sda=Pin(32))
	
	oled_width = 128
	oled_height = 64
	player_oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
	
	player_oled.text('STUDIEGRUPPE 6', 0, 0)
	player_oled.text('Booting...', 0, 30)
	player_oled.show()
	sleep(1)

player_oled_startup()

def player_battery_procentage():
    global battery_percentage
    voltage_splitter_val = 0
    for i in range(256):
        voltage_splitter_val += voltage_splitter.read()
    vs256_val = voltage_splitter_val / 256
    battery_percentage = (vs256_val - 1655) / 6.6
    battery_percentage = int(battery_percentage)
    return battery_percentage

def player_gps_location():
    if gps.receive_nmea_data():
        if gps.get_speed() != 0 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0:
            speed = str(gps.get_speed())
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            return speed + "," + lat + "," + lon + "," + "0.0"

def player_imu_tackling(imu):
	global tackling_count
	acceleration_x = imu.get_values()["acceleration_x"]
	acceleration_y = imu.get_values()["acceleration_y"]
	acceleration_z = imu.get_values()["acceleration_z"]
	sleep(0.6)
	status = False
	tackling = 0
	if acceleration_z < -14000 or acceleration_z > 15000 and not status:
		tackling_count += 1
		status = True
		sleep(0.6)
	elif acceleration_z > -14000 or acceleration_z < 15000 and status:
		status = False
	print("Tackling:", tackling_count)
	return status, tackling_count

def vibration_speed_player_5():
    for _ in range(2):
        bzz.value(1)
        sleep(0.5)
        bzz.value(0)
        sleep(0.5)
    
def vibration_speed_player_10():
    for _ in range(4):
        bzz.value(1)
        sleep(0.5)
        bzz.value(0)
        sleep(0.5)
    
def vibration_speed_player_15():
    for _ in range(6):
        bzz.value(1)
        sleep(0.5)
        bzz.value(0)
        sleep(0.5)

def vibration_speed_player_20():
    for _ in range(8):
        bzz.value(1)
        sleep(0.5)
        bzz.value(0)
        sleep(0.5)

def player_stats_adafruit():
        mqtt.web_print(player_gps_location(), 'holm/feeds/mapfeed/csv')
        sleep(3)
        mqtt.web_print(int(gps.get_speed()), 'holm/feeds/speed')
        sleep(3)
        mqtt.web_print(int(imu.get_values()["temperature celsius"]), 'holm/feeds/temp')
        sleep(3)
        mqtt.web_print(tackling_count, 'holm/feeds/tackling')
        sleep(3)
        mqtt.web_print(battery_percentage, 'holm/feeds/battery')
        sleep(3)
        mqtt.web_print(status_indicator_on, 'holm/feeds/status')
        sleep(3)
        
def player_important_functions():
    player_imu_tackling(imu)
    player_vibration_speed()
    player_gps_location
    player_battery_procentage()

def player_vibration_speed():
    global player_vibration_speed_completed_20
    global player_vibration_speed_completed_15
    global player_vibration_speed_completed_10
    global player_vibration_speed_completed_5
    speed = gps.get_speed()
    
    if speed > 20.00 and not player_vibration_speed_completed_20:
        vibration_speed_player_20()
        player_vibration_speed_completed_20 = True
        player_vibration_speed_completed_15 = False
        player_vibration_speed_completed_10 = False
        player_vibration_speed_completed_5 = False
    elif speed > 15.00 and not player_vibration_speed_completed_15:
        vibration_speed_player_15()
        player_vibration_speed_completed_15 = True
        player_vibration_speed_completed_10 = False
        player_vibration_speed_completed_5 = False
    elif speed > 10.00 and not player_vibration_speed_completed_10:
        vibration_speed_player_10()
        player_vibration_speed_completed_10 = True
        player_vibration_speed_completed_5 = False
    elif speed > 5.0 and not player_vibration_speed_completed_5:
        vibration_speed_player_5()
        player_vibration_speed_completed_5 = True

while True:
    try:
        tackling_count_value = tackling_count
        battery_percentage_value = battery_percentage
        
        player_important_functions()
        if tackling_count_value != tackling_count or battery_percentage_value != battery_percentage or player_speed_data_gps_value != gps.get_speed():
            player_oled_stats()
        player_stats_adafruit()
        
        if len(mqtt.besked) != 0: 
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO()              
   
    except KeyboardInterrupt:
        print('ctrl c pressed exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()


        