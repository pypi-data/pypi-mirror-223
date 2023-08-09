"""Process the BLE data."""


import time
import logging

import dearpygui.dearpygui as dpg

from src.ble.scanning import ble_rs

from src.globals.helpers import ThreadWithReturnValue


loggei = logging.getLogger(name=__name__)


def ble_data(company: bool) -> list:
    """Collate the da from the BLE API and return it."""
    loggei.debug(msg=f"{ble_data.__name__}()")

    target: tuple[str, str] = "rssi", "company"

    # Grab the data from the API
    data = ble_rs(
        target=target[0]
    ) if not company else ble_rs(
        target=target[1]
    )

    loggei.info(msg=data)

    # If the data is empty, return an empty dict
    if not data:
        return {}

    # Grab the data from the dict
    if not company:
        macs, rssi = (data.keys(), data.values())

    else:
        macs, companies = (data.keys(), data.values())

    return [
        list(macs),
        list(rssi)
    ] if not company else [
        list(macs),
        list(companies)
    ]


def threaded_ble_scan(company: bool) -> tuple[list]:
    """Scan for BLE signals and frequencies in a thread."""
    loggei.debug(msg=f"{threaded_ble_scan.__name__}()")

    dpg.configure_item(
        item="12",
        modal=True,
    )
    dpg.configure_item(
        item="ble_list",
        width=880,
        height=680,
    )

    dpg.add_text(
        tag="scan_text",
        default_value="SCANNING",
        pos=(400, 265)
    )

    ble = ThreadWithReturnValue(
        target=ble_data,
        args=(company[0],)
    )
    ble.start()

    ble_rssi = ThreadWithReturnValue(
        target=ble_data,
        args=(company[1],)
    )
    sleep_delay: float = 0.5

    count = 0

    while ble.is_alive():
        time.sleep(sleep_delay)
        count += 1
        dpg.configure_item(
            item="scan_text",
            default_value="SCANNING" + "." * count
        )
        count = 0 if count > 3 else count
    count = 0

    ble_rssi.start()

    while ble_rssi.is_alive():
        time.sleep(sleep_delay)
        count += 1
        dpg.configure_item(
            item="scan_text",
            default_value="SCANNING" + "." * count
        )
        count = 0 if count > 3 else count
    ble = ble.join()
    ble_rssi = ble_rssi.join()

    dpg.delete_item(item="scan_text")

    dpg.configure_item(
        item="12",
        modal=False,
    )

    return ble, ble_rssi


def ble_data_complete() -> list[tuple[str, tuple[str, str]]]:
    """Get the MAC address, Manufacturer, and RSSI."""
    company = True, False

    ble, ble_rssi = threaded_ble_scan(company=company)

    try:
        if ble[0][0] == "Status":
            loggei.error(msg="BLE API not running")
            ble = [("status", ("BLE API not running", "BLE API not running"))]
            return ble
    except IndexError as _error:
        loggei.error(msg=f"BLE fail: {_error}")
        ble = [("status", ("BLE API not running", "BLE API not running"))]
        return ble

    ble.insert(3, [])

    loggei.info("ble_company length: %s", len(ble[0]))
    loggei.info("ble_rssi length: %s", len(ble_rssi[0]))

    try:
        for i, mac in enumerate(ble_rssi[0]):
            mac = mac.split(']')[1]
            for mac_2 in ble[0]:
                if mac_2 == mac:
                    ble[2].insert(i, int(ble_rssi[-1][i]))
                    break
    except IndexError as _error:
        loggei.warning(msg=f"BLE fail: {_error}")

    for i in range(len(ble)):

        if len(ble[0]) != len(ble[2]):
            loggei.warning(msg="ble[0] != ble[2]")
            loggei.debug(msg=f"ble after insert: {ble}")

    ble = dict(zip(ble[0], zip(ble[1], ble[2])))

    ble = sorted(ble.items(), key=lambda x: x[1][1], reverse=True)

    return ble
