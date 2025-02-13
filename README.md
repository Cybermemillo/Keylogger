# Keylogger

## Descripción

Este es un keylogger forense desarrollado en Python con cifrado AES-256 para garantizar la seguridad de los registros de teclas. Su propósito es el análisis de incidentes y auditoría en entornos controlados.

## Características

- Captura las pulsaciones de teclado junto con la ventana activa en la que fueron realizadas.
- Cifra los registros con AES-256 para proteger la confidencialidad de los datos.
- Guarda los registros en archivos de log separados por día.
- Envía los logs por correo electrónico al cambiar de día.
- Permite descifrar y visualizar los registros capturados.

## Requisitos

Antes de ejecutar el keylogger, asegúrate de tener instaladas las siguientes dependencias:

```sh
pip install keyboard pycryptodome pygetwindow
```

## Archivos principales

- `keylogger.py`: Captura y cifra las pulsaciones de teclado.
- `decrypt_logs.py`: Descifra y muestra los registros capturados.
- `crypto_utils.py`: Maneja la generación de claves y el cifrado/descifrado de datos.

## Uso

### Iniciar el keylogger

Ejecuta el script principal para comenzar la captura de teclas:

```sh
python keylogger.py
```

### Descifrar registros

Para visualizar los registros cifrados, usa el siguiente comando:

```sh
python decrypt_logs.py
```

E introduce el nombre del archivo de log a descifrar cuando se solicite.

## Seguridad y Consideraciones

- Este script debe ejecutarse únicamente en entornos controlados y con propósitos forenses o de auditoría.
- No debe utilizarse para propósitos malintencionados, ya que violaría normas legales y éticas.
- Los datos capturados están cifrados para evitar accesos no autorizados.

## Posibles Futuras Mejoras

- Implementar un sistema de logs más legible con formato JSON.
- Añadir mensajes de estado en la consola para mejor seguimiento de la ejecución.
- Enviar alertas de comportamiento sospechoso a Telegram

## Licencia

Este proyecto es solo para fines educativos y de auditoría forense. Su uso indebido es responsabilidad del usuario.
