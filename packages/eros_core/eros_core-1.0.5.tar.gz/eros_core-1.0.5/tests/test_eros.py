
from eros_core import Eros, ErosLoopback
import time
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)


def test_eros_simple():
    drv = ErosLoopback(log_level=logging.DEBUG)
    eros = Eros(drv)
    
    received = []
    def callback1(data):
        print("Callback called")
        received.append(data)
        
    eros.attach_channel_callback(1, callback1)
    eros.attach_channel_callback(15, lambda x: print("Callback 2 called"))
    eros.transmit_packet(1, "Hello World")
    eros.transmit_packet(15, "Another string on another channel")
    
    time.sleep(0.1)
    
    assert received[0] == b"Hello World"

if __name__ == "__main__":
    test_eros_simple()