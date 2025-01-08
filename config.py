import solara


class Config:
    POLLING_INTERVAL = 5 * 60
    TRIG_PIN = 21
    ECHO_PIN = 20
    RELAY_ADDRESS =  0x18

    DB_CONFIG = {
        'FILE': "database.db",
        'TABLES': {
            'snapshots': """
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    gallons REAL NOT NULL
                )
            """,
            'settings': """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
        }
    }


    @staticmethod
    def get_default_settings():
        return {
            "tank_diameter": 240,
            "tank_height": 260,
            "relay_temp_on": 2,
            "relay_temp_off": 10
        }

    @staticmethod
    def initialize_settings(db_manager):
        """Initialize default settings in database"""
        for key, value in Config.get_default_settings().items():
            db_manager.update_setting(key, value)

class SolaraStore:
    #db_manager = DatabaseManager(Config.DB_FILE)
    state_relay = solara.reactive(False)
    distance_value = solara.reactive(0)
    tank_diameter = solara.reactive(260)
    tank_height = solara.reactive(240)
    relay_temp_on = solara.reactive(2)
    relay_temp_off = solara.reactive(10)
    numb_snapshots = solara.reactive(-2)

