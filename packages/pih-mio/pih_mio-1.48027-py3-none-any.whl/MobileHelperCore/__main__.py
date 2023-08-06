def start() -> None:
    from MobileHelperCore.service import Service, checker
    Service(10, checker).start()

if __name__ == '__main__':
    start()
