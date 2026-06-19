

from machine import Pin, I2C
from time import sleep
import math

# I2C0 nos pinos 4 (SDA) e 5 (SCL)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
addr = 0x68

# Acorda o MPU6050
i2c.writeto_mem(addr, 0x6B, b'\x00')

def read_raw(reg):
    high = i2c.readfrom_mem(addr, reg, 1)[0]
    low = i2c.readfrom_mem(addr, reg+1, 1)[0]
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

def get_angles():
    ax = read_raw(0x3B) / 16384
    ay = read_raw(0x3D) / 16384
    az = read_raw(0x3F) / 16384

    pitch = math.degrees(math.atan2(ax, math.sqrt(ay*ay + az*az)))
    roll  = math.degrees(math.atan2(ay, math.sqrt(ax*ax + az*az)))

    return pitch, roll

def nivel_status(pitch, roll, limite=3):
    # limite = tolerância em graus para considerar "nivelado"
    if abs(pitch) < limite and abs(roll) < limite:
        return "NIVELADO"
    status = []
    if pitch > limite:
        status.append("Frente Alta")
    elif pitch < -limite:
        status.append("Frente Baixa")
    if roll > limite:
        status.append("Direita Alta")
    elif roll < -limite:
        status.append("Esquerda Alta")
    return " | ".join(status)

print("Nível digital iniciado...")

while True:
    pitch, roll = get_angles()
    estado = nivel_status(pitch, roll)
    print(f"Pitch={pitch:6.2f}°  Roll={roll:6.2f}°  ->  {estado}")
    sleep(0.2)