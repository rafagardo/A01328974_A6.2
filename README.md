# Sistema de Reservaciones

Este proyecto es un **Sistema de Reservaciones** implementado en Python que permite gestionar hoteles, clientes y reservaciones. La aplicación utiliza archivos JSON para almacenar los datos de forma persistente y cuenta con un conjunto de pruebas unitarias para validar su correcto funcionamiento.

## Funcionalidades

### Gestión de Hoteles
- **Crear Hotel:** Permite crear un hotel nuevo asignándole un ID único, nombre, ubicación y cantidad total de habitaciones. Inicialmente, todas las habitaciones están disponibles.
- **Eliminar Hotel:** Elimina un hotel existente, identificado por su ID.
- **Mostrar Información del Hotel:** Muestra en consola los detalles del hotel.
- **Modificar Información del Hotel:** Permite actualizar los datos del hotel, incluyendo el ajuste en el número de habitaciones disponibles cuando se modifica el total.
- **Reservar Habitación:** Reserva una habitación si hay disponibilidad, decrementando el número de habitaciones disponibles.
- **Cancelar Reserva de Habitación:** Libera una habitación, incrementando la cantidad de habitaciones disponibles.

### Gestión de Clientes
- **Crear Cliente:** Permite crear un cliente nuevo asignándole un ID único, nombre, correo electrónico y teléfono.
- **Eliminar Cliente:** Elimina un cliente existente, identificado por su ID.
- **Mostrar Información del Cliente:** Muestra en consola los detalles del cliente.
- **Modificar Información del Cliente:** Permite actualizar los datos del cliente.

### Gestión de Reservaciones
- **Crear Reservación:** Crea una reservación asociando un cliente y un hotel. Al realizar la reservación, se reserva una habitación en el hotel (si hay disponibilidad).
- **Cancelar Reservación:** Cancela una reservación existente, liberando la habitación reservada en el hotel.

### Persistencia de Datos
- Los datos se almacenan en archivos JSON dentro de un directorio `data`:
  - `hotels.json` para los hoteles.
  - `customers.json` para los clientes.
  - `reservations.json` para las reservaciones.

### Manejo de Errores
- El sistema incorpora manejo de errores al leer y escribir archivos. En caso de ocurrir algún error (por ejemplo, archivos corruptos o problemas de I/O), se muestra un mensaje en consola y la ejecución continúa sin interrumpirse.

### Pruebas Unitarias
- Se han implementado pruebas unitarias utilizando el módulo `unittest` de Python. Estas pruebas cubren los principales métodos de las clases `Hotel`, `Customer` y `Reservation`, asegurando una cobertura de código superior al 85%.

### Análisis Estático y Estilo de Código
- El código sigue el estándar PEP8.
- Se recomienda usar herramientas como **flake8** y **pylint** para verificar que no existan errores o advertencias de estilo.

## Requisitos

- **Python 3.x**
- Módulos estándar: `json`, `os`, `uuid`, `datetime`
- (Opcional) Herramientas para análisis de código:
  - [flake8](https://flake8.pycqa.org/en/latest/)
  - [pylint](https://pylint.pycqa.org/en/latest/)

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://tu-repositorio-url.git
   cd tu-repositorio
