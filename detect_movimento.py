from machine import Pin, I2C
from time import sleep
import math

# I2C nos pinos 4 (SDA) e 5 (SCL)
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

    # Cálculo dos ângulos
    pitch = math.degrees(math.atan2(ax, math.sqrt(ay*ay + az*az)))
    roll  = math.degrees(math.atan2(ay, math.sqrt(ax*ax + az*az)))

    return pitch, roll

def detect_gesture(pitch, roll):
    # Ajuste fino dos limites conforme seu uso
    if roll > 25:
        return "Inclinado para a direita"
    elif roll < -25:
        return "Inclinado para a esquerda"
    elif pitch > 25:
        return "Levantando a mão"
    elif pitch < -25:
        return "Baixando a mão"
    else:
        return "Neutro"

print("Controle gestual iniciado...")

while True:
    pitch, roll = get_angles()
    gesto = detect_gesture(pitch, roll)
    print(f"Pitch={pitch:.1f}  Roll={roll:.1f}  ->  Gesto: {gesto}")
    sleep(0.2)