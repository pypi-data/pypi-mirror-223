import os
import time

import requests

from libs.in_win import config_path


class NetTools:
    @staticmethod
    def measure_ping_through_socks_proxy(
        proxy_address, proxy_address_port, target_host
    ):
        """Returns delay in milli-seconds"""
        # Set up the SOCKS proxy

        start_time = time.time()
        cmd = f"curl -s  --socks5-hostname {proxy_address}:{proxy_address_port} {target_host}"
        # print(cmd)
        out = os.popen(cmd).read()

        end_time = time.time()

        # Calculate the ping delay
        ping_delay = int(1000 * (end_time - start_time))
        return ping_delay

    @staticmethod
    def is_connected_to_internet(address="https://www.yahoo.com", lport=7595):
        proxy = {
            "http": f"socks5://127.0.0.1:{lport}",
            "https": f"socks5://127.0.0.1:{lport}",
        }

        try:
            # Attempt to send a request to a reliable website (e.g., Google) using the proxy
            response = requests.get(address, proxies=proxy, timeout=5)

            # Check if the response status code is 200 (successful)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException:
            # If an exception is raised, it means the request failed (no internet connection)
            return False


if __name__ == "__main__":
    # Replace these values with your SOCKS proxy address and the target host and port you want to ping
    # proxy_address = "127.0.0.1"
    # proxy_address_port = 7595
    # target_host = "https://google.com"
    # target_port = 80

    # ping_delay = NetTools.measure_ping_through_socks_proxy(
    #     proxy_address, proxy_address_port, target_host
    # )
    # if ping_delay is not None:
    #     print(
    #         f"Ping delay to {target_host}:{target_port} via the proxy: {ping_delay:.3f} milli-seconds"
    #     )
    print(NetTools.is_connected_to_internet())
