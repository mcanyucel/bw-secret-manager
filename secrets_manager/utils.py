# utils.py
class Colors:
    INFO = "\033[94m"    # Blue
    SUCCESS = "\033[92m" # Green
    WARN = "\033[93m"    # Yellow
    ERROR = "\033[91m"   # Red
    END = "\033[0m"      # Reset
    DEBUG = "\033[95m"   # Magenta

def info(msg):    print(f"{Colors.INFO}[INFO]{Colors.END} {msg}")
def success(msg): print(f"{Colors.SUCCESS}[SUCCESS]{Colors.END} {msg}")
def warn(msg):    print(f"{Colors.WARN}[WARN]{Colors.END} {msg}")
def error(msg):   print(f"{Colors.ERROR}[ERROR]{Colors.END} {msg}")
def debug(msg):   print(f"{Colors.DEBUG}[DEBUG]{Colors.END} {msg}")