import os, random
import inspect
import asyncio
import socket
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from loguru import logger

# This needs to be set before the first import of attacus
os.environ['FLUTTER_ASSETS'] = str(Path(__file__).parent / 'flutter_assets')
from attacus import App, FlutterView, StandardMethodChannel, StandardMethod

class MyChannel(StandardMethodChannel):
    routes = {}

    def __init__(self, messenger, name, receiver):
        super().__init__(messenger, name)
        self.receiver = receiver
        for key, value in self.routes.items():
            StandardMethod(
                self,
                key,
                lambda method_call, result: self.execute(method_call, value, result)
            )

    @classmethod
    def route(cls, method_name):
        def decorator(f):
            cls.routes[method_name] = f
            return f
        return decorator

    def execute(self, method_call, method, method_result):
        logger.debug(method_call)
        logger.debug(method)
        logger.debug(method_call.method_name())
        args = method_call.arguments()
        logger.debug(args)
        logger.debug(method_result)

        pyarg = args.decode()
        logger.debug(pyarg)
        #result = None
        if inspect.iscoroutinefunction(method):
            loop = asyncio.get_event_loop()
            def callback(future):
                result = future.result()
                logger.debug(f"Callback invoked with result: {result}")
                method_result.success(result)
            task = loop.create_task(method(self.receiver, pyarg))
            # Add the callback
            task.add_done_callback(callback)
        else:
            result = method(self.receiver, pyarg)
            method_result.success(result)

channel: StandardMethodChannel = None

class MyFlutter(FlutterView):
    def __init__(self, parent):
        super().__init__(parent)
        self.channel = None

    def startup(self):
        global channel
        super().startup()
        logger.debug("Starting up Flutter ...")
        messenger = self.messenger
        logger.debug(messenger)

        channel = self.channel = MyChannel(messenger, "logavu", self)
        logger.debug(self.channel)


    def shutdown(self):
        super().shutdown()
        logger.debug("Shutting down Flutter ...")

HOST, PORT = 'localhost', 5005

def send_test_message(message: str) -> None:
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(message.encode(), (HOST, PORT))


async def write_messages() -> None:
    print("writing")
    while True:
        delay = random.uniform(0.1, 3.0)
        logger.debug(delay)
        await asyncio.sleep(delay)
        send_test_message(str(delay))

class SyslogProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        global channel
        super().__init__()

    def connection_made(self, transport) -> None:
        self.transport = transport

    def datagram_received(self, data, addr) -> None:
        global channel
        message = data.decode()
        logger.debug(f"Received Syslog message: {message}")
        channel.invoke_method('on_message', message)


class MyApp(App):
    def __init__(self):
        super().__init__()

    def startup(self):
        super().startup()
        logger.debug("Starting up App ...")

    def loop(self):
        logger.debug("Entering App Loop ...")
        def exception_handler(loop, context):
            print(f"Caught exception: {context['exception']}")
        async def _loop(interval=1/60):
            loop = asyncio.get_event_loop()
            loop.set_exception_handler(exception_handler)

            t = loop.create_datagram_endpoint(SyslogProtocol, local_addr=('0.0.0.0', PORT))
            loop.create_task(t) # Server starts listening
            #loop.create_task(write_messages())

            while self.process_events():
                await asyncio.sleep(interval)

        asyncio.run(_loop())
        logger.debug("Exiting App Loop ...")

    def shutdown(self):
        super().shutdown()
        logger.debug("Shutting down App ...")

app = MyApp()

flutter = MyFlutter(app)

app.run()
