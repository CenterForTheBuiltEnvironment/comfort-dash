from dataclasses import asdict

from utils.database import (
    get_image_device,
    DeviceTypes,
    Device,
    User,
    Order,
    get_devices,
)


class TestGetImageDevice:
    #  Returns the path to the image file for an EMU device.
    def test_returns_path_to_emu_image_file(self):
        device = Device(
            name="EMU",
            type=DeviceTypes.emu.value,
            id="123",
            variables=["temperature", "humidity"],
        )
        assert get_image_device(device) == "./assets/media/emu.png"

    #  Returns an empty string when given an empty Device object.
    def test_returns_empty_string_for_empty_device_object(self):
        device = Device(name="", type="", id="", variables=[])
        assert get_image_device(device) == ""


class TestGetDevices:
    #  Returns a list of devices when user has orders with devices
    def test_returns_list_of_devices_when_user_has_orders_with_devices(self):
        # Arrange
        user_j = User(
            id=1,
            name="John",
            email="john@example.com",
            password="password",
            influx_url="",
            influx_username="",
            influx_password="",
            influx_database="",
        )
        user_f = User(
            id=1,
            name="fede",
            email="fede@example.com",
            password="password",
            influx_url="",
            influx_username="",
            influx_password="",
            influx_database="",
        )
        device1 = Device(
            name="Device 1", type="Type 1", id="1", variables=["var1", "var2"]
        )
        device2 = Device(
            name="Device 2", type="Type 2", id="2", variables=["var3", "var4"]
        )
        device3 = Device(
            name="Device 3", type="Type 3", id="3", variables=["var3", "var4"]
        )
        order_j = Order(devices=[device1, device2], user=user_j)
        order_f = Order(devices=[device3], user=user_f)
        orders = [order_j, order_f]

        # Act
        result = get_devices(user_j, orders)

        # Assert
        assert result == [asdict(device1), asdict(device2)]
        assert result != [asdict(device3)]

    #  Returns an empty list when orders is empty
    def test_returns_empty_list_when_orders_is_empty(self):
        # Arrange
        user = User(
            id=1,
            name="John",
            email="john@example.com",
            password="password",
            influx_url="",
            influx_username="",
            influx_password="",
            influx_database="",
        )
        orders = []

        # Act
        result = get_devices(user, orders)

        # Assert
        assert result == []
