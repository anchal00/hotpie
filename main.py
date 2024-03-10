
from hot_reload import HotReloadWatchDog
from hotpie_config import config

if __name__ == "__main__":
    HotReloadWatchDog(
        config(main_module="process")
    ).start()
