import logging.config
import sys
logging.getLogger().setLevel('DEBUG')
logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))

