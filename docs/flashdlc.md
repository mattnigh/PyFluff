# How to flash your own DLCs

## Debugging the flashing process
Before starting, I recommend you to open the 6th debug menu on Furby's LCD eyes using the `0xdb` command or through PyFluff's CLI/API. This menu will give you an overview of Furby's DLC "Slots", the memory regions where DLC files get stored.

I would assume that the `2M`, `1M`, `.5M` might be the sizes of those memory slots (2 / 1 / 0.5 Megabytes respectively), but I have not tested that. What I know, however, is that the numbers behind the `M` provide useful information for debugging the flashing process. These numbers are:
* `0` if the slot is empty, i.e. after deleting the DLC file
* `1` if the DLC file is currently being flashed / has not completed flashing, so this will be displayed if the flashing process has failed somewhere in between for some reason
* `2` if the DLC file has been successfully downloaded, but not activated yet
* `3` if the DLC file is active

## Flashing process

### Delete the old DLC file
Using PyFluff's DLC manager, delete all remaining DLC files on the Furby. The slots are enumerated as displayed on the debug menu. After this step, all debug numbers on Furby's LCD should be `0`.

```python
from pyfluff import FurbyConnect
import asyncio

async def delete_dlc():
    async with FurbyConnect.discover() as furby:
        # Delete DLC in slot 0
        await furby.delete_dlc(slot=0)
        print("DLC deleted")

asyncio.run(delete_dlc())
```

### Flash the new DLC file
Before flashing, I'd recommend you to turn on Nordic Packet ACKs. This will make Furby respond with Nordic notifications while downloading the DLC. That way, you will be able to tell if Furby is currently receiving the data you're sending. If those Nordic notifications disappear while flashing the Furby, you know that Furby has disconnected and you will have to start all over again.

For actually downloading the DLC, you can use PyFluff's DLC upload functionality:

```python
from pyfluff import FurbyConnect
from pyfluff.dlc import DLCManager
import asyncio

async def flash_dlc():
    async with FurbyConnect.discover() as furby:
        dlc_manager = DLCManager(furby)
        
        # Upload DLC file
        await dlc_manager.upload_dlc(
            file_path="path/to/your/dlc_file.dlc",
            slot=0
        )
        print("DLC uploaded successfully")

asyncio.run(flash_dlc())
```

Depending on your DLC file size, this process will take **3-5 Minutes**. Furby should display a `1` in the debug menu during upload, then a `2` when complete.

### Loading and activating
You can now load the DLC file and then activate it:

```python
from pyfluff import FurbyConnect
import asyncio

async def activate_dlc():
    async with FurbyConnect.discover() as furby:
        # Load DLC from slot
        await furby.load_dlc(slot=0)
        print("DLC loaded")
        
        # Activate the loaded DLC
        await furby.activate_dlc()
        print("DLC activated")

asyncio.run(activate_dlc())
```

After this, Furby's debug screen should show a `3` for the respective slot. The actions / songs in the DLC file should now be available through action input `75`, e.g. input 75, index 0, subindex 0 and specific 0. See [Action Sequences](actions.md) for information on how to trigger those songs and reactions.

## Using the CLI

PyFluff also provides a CLI interface for DLC management:

```bash
# Upload a DLC file
pyfluff dlc upload path/to/file.dlc --slot 0

# Load a DLC
pyfluff dlc load --slot 0

# Activate the loaded DLC
pyfluff dlc activate

# Deactivate a DLC
pyfluff dlc deactivate --slot 0

# Delete a DLC
pyfluff dlc delete --slot 0
```

> [!NOTE]
> This documentation is derived from the [bluefluff project](https://github.com/Jeija/bluefluff) by Jeija. The original research and reverse engineering work was done by the bluefluff community. PyFluff is a modern Python implementation of the same protocols.