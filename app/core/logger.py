import logging

# Logger global para toda la app
logger = logging.getLogger("financial-api")
logger.setLevel(logging.INFO)

# Formato: timestamp, nivel, módulo, mensaje
formatter = logging.Formatter(
    "%(asctime)s — %(levelname)s — %(name)s — %(message)s"
)

# Handler de consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
