import asyncio
import tempfile
import pathlib

class UDPMeasureServerProtocol:
    def __init__(self, tmpdir, basename):
        self.tmpdir = tmpdir
        self.basename = basename
        self._save_f_cnt = 0

    def connection_made(self, transport):
        self.transport = transport
        self.tmpfpath = pathlib.Path(self.tmpdir)
        self.tmpfpath = self.tmpfpath / self.basename
        self.f = open(str(self.tmpfpath), "w+")

    def datagram_received(self, data, addr):

        message = data.decode()

        print('Received %r from %s' % (message, addr), file=self.f)
        self.f.flush()

        print('Received %r from %s' % (message, addr))
        print('file size:', self.tmpfpath.stat().st_size)

        if self.tmpfpath.stat().st_size > 2000:
            self.f.close()
            print("A file has been closed.")
            self._save_f_cnt += 1

            if self._save_f_cnt >= 2:
                self.f.close()
                print("A file has been closed.")
                self.transport.close()
            else:
                self.tmpfpath = self.tmpfpath.parent / (str(self.tmpfpath.stem) + str(self._save_f_cnt + 1) + str(self.tmpfpath.suffix))
                self.f = open(str(self.tmpfpath), "w+")
        else:
            print(self.tmpfpath.stat().st_size)

    def connection_lost(self, exc):

        p_tmpdir = pathlib.Path(self.tmpdir)
        for p_log in p_tmpdir.glob('*.log'):
            _f = open(str(p_log), "r")
            print("File name:", str(p_log))
            print(_f.read(), end="\n")
            _f.close()

        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

    def error_received(self, exc):
        print('Error received:', exc)
        self.transport.close()

    def eof_received(self):
        self.transport.close()


# One protocol instance will be created to serve all client requests
with tempfile.TemporaryDirectory() as dname:
    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    listen = loop.create_datagram_endpoint(
        lambda: UDPMeasureServerProtocol(dname, "measure.log"), local_addr=('127.0.0.1', 9999))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Raised KeyboardInterrupt!!")
        pass

    transport.close()
    loop.close()
    print("Ending UDP server")