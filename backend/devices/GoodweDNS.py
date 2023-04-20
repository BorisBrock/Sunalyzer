import requests
import logging
import socket
from datetime import datetime
from collections import namedtuple
import struct


# this implementation borrows very heavily from https://github.com/borft/py-goodwe
# and https://github.com/marcelblijleven/goodwe

# Goodwe devices
class GoodweDNS:
    def __init__(self, config, _id):
        # Demo code for config access
        hostname_configured = False
        try:
            self.host_name = config.config_data[_id]['host_name']  # use _id to get the "device2" section
        except KeyError:
            logging.info(f"Grabber: Goodwe device does not have a hostname in the '{_id}:' section of config.yaml")
        except Exception as e:
            logging.exception(e)
        else:
            hostname_configured = True

        if hostname_configured is False:
            try:
                self.host_name = config.config_data['goodwe_dns']['host_name']
            except KeyError:
                logging.info(f"Grabber: config.yaml does not contain a hostname for "
                             f"{config.config_data[_id]['type']} declared in section '{_id}:'")
                raise
            except Exception as e:
                logging.exception(e)
            else:
                logging.info(f"Grabber: took host_name from the 'goodwe_dns:' section in config.yaml."
                             f" Please move option to the '{_id}:' section instead")

        self.goodwe_port = 8899
        self.last_response = datetime.now()

        logging.info(f"GoodweDNS device: "
                     f"configured host name is "
                     f"{self.host_name}")

        self.specific_option = config.config_data['goodwe_dns']['specific_option']  # not currently used

        # Initialize with default values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
        self.total_energy_consumed_from_grid_kwh = 0.0

        self.current_power_produced_kw = 0.0
        self.current_power_consumed_from_grid_kw = 0.0
        self.current_power_consumed_from_pv_kw = 0.0
        self.current_power_consumed_total_kw = 0.0
        self.current_power_fed_in_kw = 0.0

        self.run_data = namedtuple('GoodweDNS', '\
            year \
            month \
            day \
            hour \
            minute \
            second \
            vpv1 \
            ipv1 \
            vpv2 \
            ipv2 \
            vpv3 \
            ipv3 \
            vpv4 \
            ipv4 \
            vpv5 \
            ipv5 \
            ipv6 \
            vpv6 \
            vline1 \
            vline2 \
            vline3 \
            vgrid1 \
            vgrid2 \
            vgrid3 \
            igrid1 \
            igrid2 \
            igrid3 \
            fgrid1 \
            fgrid2 \
            fgrid3 \
            xx54 \
            ppv \
            work_mode \
            error_codes \
            warning_code \
            xx66 \
            xx68 \
            xx70 \
            xx72 \
            xx74 \
            xx76 \
            xx78 \
            xx80 \
            temperature \
            xx84 \
            xx86 \
            e_day \
            e_total \
            h_total \
            safety_country \
            xx100 \
            xx102 \
            xx104 \
            xx106 \
            xx108 \
            xx110 \
            xx112 \
            xx114 \
            xx116 \
            xx118 \
            xx120 \
            xx122 \
            funbit \
            vbus \
            vnbus \
            xx130 \
            xx132 \
            xx134 \
            xx136 \
            xx138')

        self.format_list = '!BBBBBBHHHHHHHHHHHHHHHHHHhhhHHHHHHLHHHHHHHHHHHHHLLHHHHHHHHHHHHHHHHHHHHH'

        # Test connection by doing an initial update
        try:
            self.update()
        except Exception:
            logging.error(
                "Goodwe device: Error: connecting to the device failed")
            # raise  # disable the raise since goodwe inverters go offline if the panels are not producing power

    def update(self):
        '''Updates all device stats.'''
        try:
            # Query inverter received_data
            # inverter = await goodwe.connect(self.host_name)
            runtime_data = self.getData()

            runtime_values = self.run_data._make(struct.unpack_from(self.format_list, runtime_data, 3))

            # Store results
            self.current_power_produced_kw = runtime_values.ppv / 1000
            self.total_energy_produced_kwh = runtime_values.e_total / 10
            logging.debug(f'Data received for power [{runtime_values.ppv}] and production [{runtime_values.e_total}]')
            logging.debug(f'Set power to {self.current_power_produced_kw} kW '
                          f'and production to {self.total_energy_produced_kwh} kWh')

        except requests.exceptions.Timeout:
            logging.error(f"Goodwe device: Timeout requesting "
                          f"'{self.url_inverter}' or '{self.url_meter}'")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Goodwe device: requests exception {e} for URL "
                          f"'{self.url_inverter}' or '{self.url_meter}'")
            raise

    @staticmethod
    def getCRC(run_data_bytes: list[bytes]) -> list[bytes]:
        crc = 0xFFFF
        odd = False

        for i in range(0, len(run_data_bytes)):
            crc ^= run_data_bytes[i]

            for j in range(0, 8):
                odd = (crc & 0x0001) != 0
                crc >>= 1
                if odd:
                    crc ^= 0xA001
        return crc.to_bytes(2, byteorder='little', signed=False)

    def getData(self, retries=3):
        while retries > 0:
            retries -= 1
            try:
                return self._getData(self.host_name, self.goodwe_port)
            except Exception as e:
                logging.debug(f'Retrying {retries} {e}')
                if datetime.now().timestamp() - self.last_response.timestamp() > 60:
                    self.current_power_produced_kw = 0
                pass
        raise Exception('Could not get proper received_data after retrying')

    def _getData(self, ip, port):

        # get received_data from inverter
        udp_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_connection.settimeout(1)
        runtime_query = bytes(b'\x7f\x03\x75\x94\x00\x49\xd5\xc2')
        udp_connection.sendto(runtime_query, (ip, port))   # TODO; handle exception

        response = udp_connection.recvfrom(1024)
        logging.debug(f'Got response from server: {response}')
        self.last_response = datetime.now()

        # the first part is a list of bytes
        received_data = bytes(response[0])

        # check length of packet
        if len(received_data) != 153:
            raise Exception(f'Data received was not usable (unexpected length: {len(received_data)}')

        # check header
        header = received_data[0:2]
        if header != b'\xaa\x55':
            raise Exception(f'Data received has invalid header: {header}')

        # check CRC
        receivedCRC = received_data[-2:]
        run_data_bytes = received_data[2:151]
        calculatedCRC = self.getCRC(run_data_bytes)
        if receivedCRC != calculatedCRC:
            raise Exception(f'CRC error: received {receivedCRC}, calulated {calculatedCRC}')

        return run_data_bytes
