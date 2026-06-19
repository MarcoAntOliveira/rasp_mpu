from machine import Pin, I2C
from time import sleep

MPU_ADDR = 0x68

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

# Acorda o MPU6050
i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')

def read_raw(reg):
    high = i2c.readfrom_mem(MPU_ADDR, reg, 1)[0]
    low = i2c.readfrom_mem(MPU_ADDR, reg+1, 1)[0]
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

while True:
    ax = read_raw(0x3B) / 16384
    ay = read_raw(0x3D) / 16384
    az = read_raw(0x3F) / 16384

    gx = read_raw(0x43) / 131
    gy = read_raw(0x45) / 131
    gz = read_raw(0x47) / 131

    print("Aceleração (g):", ax, ay, az)
    print("Giroscópio (°/s):", gx, gy, gz)
    print("-----")
    sleep(0.5)