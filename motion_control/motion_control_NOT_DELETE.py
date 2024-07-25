import serial
import time

# Замените 'COMX' на имя вашего последовательного порта
ser = serial.Serial('COMX', 9600, timeout=1)
time.sleep(2)  # Ждем, пока Arduino сбросится

while True:
    a = int(input("Введите линейную скорость (-100 до 100): "))
    b = int(input("Введите угловую скорость (-100 до 100): "))

    # Ограничиваем значения a и b в диапазоне от -100 до 100
    a = max(-100, min(100, a))
    b = max(-100, min(100, b))

    # Отправляем значения a и b на Arduino
    ser.write(f"{a},{b}\n".encode())
    time.sleep(0.1)  # Ждем, пока Arduino обработает данные
