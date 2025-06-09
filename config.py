import os, json, hashlib
from filelock import FileLock
try:
    from simcard import load_config_from_sim, save_config_to_sim
    SIM_AVAILABLE = True
except ImportError:
    SIM_AVAILABLE = False

CONFIG = os.path.join(os.path.dirname(__file__), 'config.json')
LOCK = CONFIG + '.lock'

DEFAULT = {"pin_salt": None, "pin_hash": None, "api_key": None}


def load_config():
    if SIM_AVAILABLE:
        try:
            return json.loads(load_config_from_sim())
        except Exception:
            pass
    if not os.path.exists(CONFIG):
        save_config(DEFAULT)
    with FileLock(LOCK):
        return json.load(open(CONFIG))


def save_config(cfg):
    txt = json.dumps(cfg, indent=2)
    if SIM_AVAILABLE:
        try:
            save_config_to_sim(txt)
            return
        except:
            pass
    with FileLock(LOCK):
        open(CONFIG, 'w').write(txt)


def set_pin(pin):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', pin.encode(), salt, 200000)
    cfg = load_config(); cfg['pin_salt']=salt.hex(); cfg['pin_hash']=dk.hex()
    save_config(cfg)


def verify_pin(pin):
    cfg=load_config(); salt=cfg.get('pin_salt')
    if not salt: return False
    dk=hashlib.pbkdf2_hmac('sha256', pin.encode(), bytes.fromhex(salt),200000)
    return dk.hex()==cfg.get('pin_hash')