import os
import sys

from modules.master import start_master
from modules.processor import start_processor

allowed_roles = ["master", "processor"]
role = "processor"

if len(sys.argv) >= 2:
    role = sys.argv[1]
elif "GH_POC_ROLE" in os.environ:
    role = os.environ["GH_POC_ROLE"]

if role in allowed_roles:
    if role == 'master':
        start_master()
    elif role == 'processor':
        start_processor()
else:
    print("Unknown role: %s" % role)
