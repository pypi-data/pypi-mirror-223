from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


class Discovery:
    def __init__(self, callback):
        self.callback = callback
        self.zeroconf = Zeroconf()
        self.listener = Discovery._Listener(callback)
        self.browser = ServiceBrowser(self.zeroconf, "_eagle._tcp.local.", self.listener)

    def stop(self):
        self.browser.cancel()
        self.zeroconf.close()
    
    class _Listener(ServiceListener):
        def __init__(self, callback):
            self.callback = callback

        def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            pass

        def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            pass

        def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            self.callback(name)
