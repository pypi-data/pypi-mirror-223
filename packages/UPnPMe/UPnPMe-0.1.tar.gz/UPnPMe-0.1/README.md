**English Documentation:**

# UPnPMe Documentation

## Introduction

UPnPMe is a simple Python script that allows you to configure port forwarding using the UPnP (Universal Plug and Play) protocol. With UPnPMe, you can easily add port mappings to UPnP-enabled devices.

## Usage

To use UPnPMe, follow these steps:

1. Create a Python environment (recommended).
2. Install UPnPMe using the following command line: "pip install UPnPMe".
3. Import the library in your Python script using: `from upnpme import add_port_forwarding`.
4. Use the `add_port_forwarding` function to add port forwarding.

## Example

```python
# Example Script using UPnPMe

from upnpme import add_port_forwarding

def main():
    # Example parameters
    target_ip = ""  # Empty for local machine's IP
    gateway_ip = "192.168.1.1"
    external_port = 12345
    internal_port = 12345
    protocol = "TCP"

    success = add_port_forwarding(target_ip, gateway_ip, external_port, internal_port, protocol)
    if success:
        print("Port forwarding added successfully.")
    else:
        print("Failed to add port forwarding.")

if __name__ == "__main__":
    main()
```

**Note:** Created by Facundo García Payer to the world.

---

**Documentación en Español:**

# Documentación de UPnPMe

## Introducción

UPnPMe es un simple script de Python que te permite configurar el reenvío de puertos utilizando el protocolo UPnP (Universal Plug and Play). Con UPnPMe, puedes añadir fácilmente mapeos de puertos a dispositivos habilitados para UPnP.

## Uso

Para usar UPnPMe, sigue estos pasos:

1. Crea un entorno de Python (recomendado).
2. Instalar UPnPMe usando el siguiente comando: "pip install UPnPMe".
3. Importa la librería en tu script de Python usando: `from upnpme import add_port_forwarding`.
4. Utiliza la función `add_port_forwarding` para añadir el reenvío de puertos.

## Ejemplo

```python
# Script de Ejemplo usando UPnPMe

from upnpme import add_port_forwarding

def main():
    # Parámetros de ejemplo
    target_ip = ""  # Vacío para la IP local de la máquina
    gateway_ip = "192.168.1.1"
    external_port = 12345
    internal_port = 12345
    protocol = "TCP"

    success = add_port_forwarding(target_ip, gateway_ip, external_port, internal_port, protocol)
    if success:
        print("Reenvío de puertos añadido exitosamente.")
    else:
        print("Error al añadir el reenvío de puertos.")

if __name__ == "__main__":
    main()
```

**Nota:** Creado por Facundo García Payer para el mundo.
