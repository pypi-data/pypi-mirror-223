class Size:
    IV: int = 16
    SALT: int = 16
    PEPPER: int = 16
    BLOCK: int = 16
    MAIN_KEY: int = 32
    AES_KEY: int = 32
    HMAC: int = 32
    MIN_ITERATIONS: int = 50
    MAX_ITERATIONS: int = 10**6


class Gui:
    THEME: str = 'vapor'
    TITLE: str = 'ashcrypt'
    DIMENSIONS: str = '1500x800'
