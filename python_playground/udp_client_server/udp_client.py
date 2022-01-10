import asyncio

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        try:
            for i in range(10):
                self.transport.sendto((str(i) + ': ' + self.message).encode())
        finally:
            # self.transport.write_eof()
            self.transport.close()

    def datagram_received(self, data, addr):
        print("Received:", data.decode())
        self.transport.close()
        print("Close the socket")


    def error_received(self, exc):
        print('Error received:', exc)
        self.transport.close()

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()


loop = asyncio.get_event_loop()
message = "Hello World!"
connect = loop.create_datagram_endpoint(
    lambda: EchoClientProtocol(message, loop),
    remote_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(connect)
try:
    loop.run_forever()
except:
    print("Exception was caused!")
finally:
    transport.close()
    loop.close()