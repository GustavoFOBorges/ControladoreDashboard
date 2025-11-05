  GNU nano 7.2                                          agent2.py                                                   import psutil
import time
import requests
import platform

SERVER_URL = "http://10.69.32.14:5001/update"  # IP do servidor central
SERVER_NAME = "Servidor Web"  # Troque para o correspondente

def get_temp():
    """
    Retorna a temperatura da CPU se disponível.
    """
    temps = psutil.sensors_temperatures()
    if temps:
        # Pega a primeira temperatura disponível
        for name, entries in temps.items():
            return entries[0].current
    return None  # Se não houver sensor

def get_uptime():
    """
    Retorna tempo de atividade do sistema em horas:minutos.
    """
    uptime_seconds = time.time() - psutil.boot_time()
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    return f"{hours}h {minutes}m"

while True:
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    data = {
        "name": SERVER_NAME,
        "cpu": psutil.cpu_percent(),
        "ram": ram.percent,
        "ram_used": round(ram.used / (1024**3)),      # GB usados
        "ram_total": round(ram.total / (1024**3)),    # GB total
        "disk": disk.percent,
        "disk_used": round(disk.used / (1024**3)),    # GB usados
        "disk_total": round(disk.total / (1024**3)),  # GB total
        "temp": get_temp(),
        "uptime": get_uptime()
    }

    try:
        requests.post(SERVER_URL, json=data)
    except Exception as e:
        print("Erro ao enviar dados:", e)


    time.sleep(5)
