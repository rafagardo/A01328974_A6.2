#!/usr/bin/env python3
"""
Módulo principal del sistema de reservaciones.
Contiene las clases Hotel, Customer y Reservation,
además de funciones auxiliares para la persistencia en archivos.
"""

import json
import os
import uuid
from datetime import datetime

# Constantes de archivos y directorio de datos
DATA_DIR = "data"
HOTELS_FILE = os.path.join(DATA_DIR, "hotels.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.json")


def ensure_data_files():
    """Crea el directorio de datos y los archivos JSON si no existen."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for file_path in [HOTELS_FILE, CUSTOMERS_FILE, RESERVATIONS_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f)


def load_data(file_path):
    """
    Carga datos desde el archivo especificado.
    Si ocurre un error, muestra el error en consola y retorna una lista vacía.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, IOError) as error:
        print(f"Error leyendo {file_path}: {error}")
        return []


def save_data(file_path, data):
    """
    Guarda los datos en el archivo especificado.
    Si ocurre un error, muestra el error en consola.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError as error:
        print(f"Error escribiendo {file_path}: {error}")


class Hotel:
    """Clase que representa un hotel."""

    def __init__(self, hotel_id, name, location, total_rooms, available_rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = available_rooms

    @classmethod
    def create_hotel(cls, name, location, total_rooms):
        """
        Crea un hotel nuevo y lo guarda en el archivo correspondiente.
        Se asigna un id único y se inicializan las habitaciones disponibles.
        """
        hotel_id = str(uuid.uuid4())
        new_hotel = cls(hotel_id, name, location, total_rooms, total_rooms)
        hotels = load_data(HOTELS_FILE)
        hotels.append(new_hotel.__dict__)
        save_data(HOTELS_FILE, hotels)
        return new_hotel

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel identificado por su id."""
        hotels = load_data(HOTELS_FILE)
        updated_hotels = [h for h in hotels if h.get("hotel_id") != hotel_id]
        if len(updated_hotels) == len(hotels):
            print("Hotel no encontrado")
        else:
            save_data(HOTELS_FILE, updated_hotels)
            print("Hotel eliminado correctamente")

    @classmethod
    def get_hotel(cls, hotel_id):
        """Retorna una instancia de Hotel a partir de su id,
        o None si no se encuentra."""
        hotels = load_data(HOTELS_FILE)
        for h in hotels:
            if h.get("hotel_id") == hotel_id:
                return cls(**h)
        print("Hotel no encontrado")
        return None

    def display_info(self):
        """Muestra la información del hotel en consola."""
        info = (
            f"Hotel ID: {self.hotel_id}\n"
            f"Nombre: {self.name}\n"
            f"Ubicación: {self.location}\n"
            f"Habitaciones Totales: {self.total_rooms}\n"
            f"Habitaciones Disponibles: {self.available_rooms}"
        )
        print(info)

    def modify_info(self, name=None, location=None, total_rooms=None):
        """
        Modifica la información del hotel. Si se
        modifica el total de habitaciones, se
        ajustan las habitaciones disponibles en
        consecuencia.
        """
        if name:
            self.name = name
        if location:
            self.location = location
        if total_rooms is not None:
            difference = total_rooms - self.total_rooms
            self.total_rooms = total_rooms
            self.available_rooms += difference
            if self.available_rooms < 0:
                self.available_rooms = 0
        hotels = load_data(HOTELS_FILE)
        for h in hotels:
            if h.get("hotel_id") == self.hotel_id:
                h.update(self.__dict__)
                break
        save_data(HOTELS_FILE, hotels)

    def reserve_room(self):
        """
        Reserva una habitación si hay
        disponibles. Disminuye el número
        de habitaciones disponibles y
        actualiza el archivo.
        """
        if self.available_rooms > 0:
            self.available_rooms -= 1
            hotels = load_data(HOTELS_FILE)
            for h in hotels:
                if h.get("hotel_id") == self.hotel_id:
                    h["available_rooms"] = self.available_rooms
                    break
            save_data(HOTELS_FILE, hotels)
            return True
        print("No hay habitaciones disponibles")
        return False

    def cancel_room(self):
        """
        Cancela una reserva, incrementando
        el número de habitaciones disponibles.
        """
        if self.available_rooms < self.total_rooms:
            self.available_rooms += 1
            hotels = load_data(HOTELS_FILE)
            for h in hotels:
                if h.get("hotel_id") == self.hotel_id:
                    h["available_rooms"] = self.available_rooms
                    break
            save_data(HOTELS_FILE, hotels)
            return True
        print("Todas las habitaciones ya están disponibles")
        return False


class Customer:
    """Clase que representa un cliente."""

    def __init__(self, customer_id, name, email, phone):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    @classmethod
    def create_customer(cls, name, email, phone):
        """Crea un cliente nuevo y lo guarda en el archivo correspondiente."""
        customer_id = str(uuid.uuid4())
        new_customer = cls(customer_id, name, email, phone)
        customers = load_data(CUSTOMERS_FILE)
        customers.append(new_customer.__dict__)
        save_data(CUSTOMERS_FILE, customers)
        return new_customer

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente identificado por su id."""
        customers = load_data(CUSTOMERS_FILE)
        updated_customers = [
            c for c in customers if c.get("customer_id") != customer_id
        ]
        if len(updated_customers) == len(customers):
            print("Cliente no encontrado")
        else:
            save_data(CUSTOMERS_FILE, updated_customers)
            print("Cliente eliminado correctamente")

    @classmethod
    def get_customer(cls, customer_id):
        """Retorna una instancia de Customer a partir de su id,
        o None si no se encuentra."""
        customers = load_data(CUSTOMERS_FILE)
        for c in customers:
            if c.get("customer_id") == customer_id:
                return cls(**c)
        print("Cliente no encontrado")
        return None

    def display_info(self):
        """Muestra la información del cliente en consola."""
        info = (
            f"Cliente ID: {self.customer_id}\n"
            f"Nombre: {self.name}\n"
            f"Email: {self.email}\n"
            f"Teléfono: {self.phone}"
        )
        print(info)

    def modify_info(self, name=None, email=None, phone=None):
        """Modifica la información del cliente y actualiza el archivo."""
        if name:
            self.name = name
        if email:
            self.email = email
        if phone:
            self.phone = phone
        customers = load_data(CUSTOMERS_FILE)
        for c in customers:
            if c.get("customer_id") == self.customer_id:
                c.update(self.__dict__)
                break
        save_data(CUSTOMERS_FILE, customers)


class Reservation:
    """Clase que representa una reservación."""

    def __init__(self, reservation_id, customer_id,
                 hotel_id, reservation_date):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.reservation_date = reservation_date

    @classmethod
    def create_reservation(cls, customer_instance, hotel_instance):
        """
        Crea una reservación vinculando un cliente y un hotel.
        Se valida que los parámetros sean instancias de
        Customer y Hotel.
        """
        if not isinstance(customer_instance,
                          Customer) or not isinstance(hotel_instance,
                                                      Hotel):
            print("Cliente u hotel inválido")
            return None
        if not hotel_instance.reserve_room():
            print("La reserva de habitación falló")
            return None
        reservation_id = str(uuid.uuid4())
        reservation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_reservation = cls(reservation_id, customer_instance.customer_id,
                              hotel_instance.hotel_id, reservation_date)
        reservations = load_data(RESERVATIONS_FILE)
        reservations.append(new_reservation.__dict__)
        save_data(RESERVATIONS_FILE, reservations)
        return new_reservation

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """
        Cancela una reservación identificada por su id,
        liberando la habitación en el hotel.
        """
        reservations = load_data(RESERVATIONS_FILE)
        reservation_to_cancel = None
        for r in reservations:
            if r.get("reservation_id") == reservation_id:
                reservation_to_cancel = r
                break
        if reservation_to_cancel is None:
            print("Reservación no encontrada")
            return False
        hotel_instance = Hotel.get_hotel(reservation_to_cancel.get("hotel_id"))
        if hotel_instance:
            hotel_instance.cancel_room()
        updated_reservations = [
            r for r in reservations if r.get("reservation_id") != reservation_id
        ]
        save_data(RESERVATIONS_FILE, updated_reservations)
        print("Reservación cancelada correctamente")
        return True

    def display_info(self):
        """Muestra la información de la reservación en consola."""
        info = (
            f"Reservación ID: {self.reservation_id}\n"
            f"Cliente ID: {self.customer_id}\n"
            f"Hotel ID: {self.hotel_id}\n"
            f"Fecha: {self.reservation_date}"
        )
        print(info)


if __name__ == "__main__":
    # Inicializa el sistema creando los archivos de datos si no existen.
    ensure_data_files()

    # Ejemplo de uso en consola:
    print("=== Creación de Hotel ===")
    hotel = Hotel.create_hotel("Hotel Central", "Ciudad X", 20)
    hotel.display_info()

    print("\n=== Creación de Cliente ===")
    customer = Customer.create_customer("Ana Pérez",
                                        "ana@example.com",
                                        "555-1234")
    customer.display_info()

    print("\n=== Creación de Reservación ===")
    reservation = Reservation.create_reservation(customer, hotel)
    if reservation:
        reservation.display_info()
