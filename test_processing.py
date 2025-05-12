import socket
import time
import math
import threading
import pygame

# Konfiguration
SEND_IP = "127.0.0.1"
SEND_PORT = 45682
SEND_INTERVAL = 0.1  # 10 Hz

# Startposition (Nähe Manching)
lat = 48.76333
lon = 11.46167
alt = 450.0  # Meter
heading = 0.0  # Grad
speed = 0.0  # m/s

msg_id = 0

# Umrechnungsfaktor für 1m in Längen-/Breitengrad (grob, für Manching)
METER_TO_LAT = 1 / 111111
METER_TO_LON = 1 / (111111 * math.cos(math.radians(lat)))

# Tasteneingabe-Thread starten
pygame.init()
screen = pygame.display.set_mode((400, 100))
pygame.display.set_caption("WASD Aircraft Control")

# UDP-Socket einrichten
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Geschwindigkeit und Steuerung
speed_delta = 2.0     # m/s pro Tastendruck
turn_rate = 10.0      # Grad pro Tastendruck

# Positionsupdate in Thread
def update_position():
    global lat, lon, heading, speed, msg_id
    last_time = time.time()

    while True:
        now = time.time()
        dt = now - last_time
        last_time = now

        # Bewegung berechnen (einfache Vorwärtsbewegung)
        distance = speed * dt
        dx = math.sin(math.radians(heading)) * distance
        dy = math.cos(math.radians(heading)) * distance


        lat += dy * METER_TO_LAT
        lon += dx * METER_TO_LON

        # Nachricht formatieren und senden
        msg_id += 1
        msg = f"{msg_id},{lat:.6f},{lon:.6f},{alt:.1f},{heading:.1f}"
        sock.sendto(msg.encode(), (SEND_IP, SEND_PORT))

        time.sleep(SEND_INTERVAL)

# Thread starten
threading.Thread(target=update_position, daemon=True).start()

# Hauptloop für Tastatursteuerung
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        speed += speed_delta
    if keys[pygame.K_s]:
        speed -= speed_delta
    if keys[pygame.K_a]:
        heading -= turn_rate
    if keys[pygame.K_d]:
        heading += turn_rate

    # Begrenzung
    speed = max(0.0, min(speed, 150.0))
    heading = heading % 360

    screen.fill((30, 30, 30))
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Speed: {speed:.1f} m/s   Heading: {heading:.1f}°", True, (255, 255, 255))
    screen.blit(text, (20, 40))
    pygame.display.flip()

    time.sleep(0.05)

pygame.quit()
