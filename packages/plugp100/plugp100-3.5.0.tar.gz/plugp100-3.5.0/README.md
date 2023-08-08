# Plug P100
This is a fork of original work of [@K4CZP3R](https://github.com/K4CZP3R/tapo-p100-python)

The purpose of this fork is to provide the library as PyPi package. 

# How to install
```pip install plugp100```

# Code example

```python
import asyncio

from plugp100 import TapoApiClient, TapoApiClientConfig
from plugp100.api.light_effect import LightEffectPreset


async def main():
    # create generic tapo api
    config = TapoApiClientConfig("<ip>", "<email>", "<passwd>")
    sw = TapoApiClient.from_config(config)
    await sw.login()
    await sw.off()
    state = await sw.get_state()
    print(state.firmware_version)
    print(state.is_hardware_v2)

    # color temperature and brightness
    await sw.set_color_temperature(4000)
    await sw.set_brightness(100)

    # light effect example
    await sw.set_light_effect(LightEffectPreset.rainbow().effect)
    state = await sw.get_state()
    print(state.get_unmapped_state())
    print(state.get_unmapped_state())
    print(state.get_energy_unmapped_state())
    print(state.get_semantic_firmware_version())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()

```

