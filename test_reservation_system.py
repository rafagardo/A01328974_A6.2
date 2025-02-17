#!/usr/bin/env python3
"""
Módulo de pruebas unitarias para el sistema de reservaciones.
Se utiliza el módulo unittest para testear los métodos de Hotel,
Customer y Reservation.
"""

import os
import shutil
import tempfile
import unittest

from reservation_system import (
    ensure_data_files,
    Hotel,
    Customer,
    Reservation,
    DATA_DIR,
)

HOTELS_FILE = None
CUSTOMERS_FILE = None
RESERVATIONS_FILE = None


class TestReservationSystem(unittest.TestCase):
    """Casos de prueba para el sistema de reservaciones."""

    def setUp(self):
        # Crea un directorio temporal para los datos de prueba.
        self.test_dir = tempfile.mkdtemp()
        # Redefine las rutas globales para apuntar al directorio temporal.
        global DATA_DIR, HOTELS_FILE, CUSTOMERS_FILE, RESERVATIONS_FILE
        DATA_DIR = self.test_dir
        HOTELS_FILE = os.path.join(DATA_DIR, "hotels.json")
        CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
        RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.json")
        ensure_data_files()

    def tearDown(self):
        # Elimina el directorio temporal después de cada prueba.
        shutil.rmtree(self.test_dir)

    def test_create_and_display_hotel(self):
        hotel = Hotel.create_hotel("Test Hotel", "Test City", 10)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.name, "Test Hotel")
        self.assertEqual(hotel.location, "Test City")
        self.assertEqual(hotel.total_rooms, 10)
        self.assertEqual(hotel.available_rooms, 10)

    def test_modify_hotel(self):
        hotel = Hotel.create_hotel("Hotel A", "City A", 5)
        hotel.modify_info(name="Hotel B", total_rooms=8)
        updated_hotel = Hotel.get_hotel(hotel.hotel_id)
        self.assertEqual(updated_hotel.name, "Hotel B")
        self.assertEqual(updated_hotel.total_rooms, 8)
        # Se espera que available_rooms se ajuste (de 5 a 8)
        self.assertEqual(updated_hotel.available_rooms, 8)

    def test_delete_hotel(self):
        hotel = Hotel.create_hotel("Hotel Delete", "City", 5)
        Hotel.delete_hotel(hotel.hotel_id)
        self.assertIsNone(Hotel.get_hotel(hotel.hotel_id))

    def test_reserve_and_cancel_room(self):
        hotel = Hotel.create_hotel("Hotel Reserve", "City", 2)
        result = hotel.reserve_room()
        self.assertTrue(result)
        self.assertEqual(hotel.available_rooms, 1)
        result_cancel = hotel.cancel_room()
        self.assertTrue(result_cancel)
        self.assertEqual(hotel.available_rooms, 2)

    def test_create_and_modify_customer(self):
        customer = Customer.create_customer(
            "John Doe", "john@example.com", "1234567890"
        )
        self.assertEqual(customer.name, "John Doe")
        customer.modify_info(name="Jane Doe", email="jane@example.com")
        updated_customer = Customer.get_customer(customer.customer_id)
        self.assertEqual(updated_customer.name, "Jane Doe")
        self.assertEqual(updated_customer.email, "jane@example.com")

    def test_delete_customer(self):
        customer = Customer.create_customer(
            "Delete Customer", "del@example.com", "0987654321"
        )
        Customer.delete_customer(customer.customer_id)
        self.assertIsNone(Customer.get_customer(customer.customer_id))

    def test_create_and_cancel_reservation(self):
        hotel = Hotel.create_hotel("Res Hotel", "Res City", 1)
        customer = Customer.create_customer(
            "Res Customer", "res@example.com", "1112223333"
        )
        reservation = Reservation.create_reservation(customer, hotel)
        self.assertIsNotNone(reservation)
        # Tras la reservación, no deben quedar habitaciones disponibles
        updated_hotel = Hotel.get_hotel(hotel.hotel_id)
        self.assertEqual(updated_hotel.available_rooms, 0)
        # Cancelar la reservación debe liberar la habitación
        result = Reservation.cancel_reservation(reservation.reservation_id)
        self.assertTrue(result)
        updated_hotel = Hotel.get_hotel(hotel.hotel_id)
        self.assertEqual(updated_hotel.available_rooms, 1)

    def test_invalid_reservation(self):
        # Intentar crear una reservación con parámetros inválidos
        reservation = Reservation.create_reservation("not_customer",
                                                     "not_hotel")
        self.assertIsNone(reservation)


if __name__ == "__main__":
    unittest.main()
