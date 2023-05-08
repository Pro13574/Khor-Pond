from Pond import Pond

from FishStore import FishStore, connect_to_redis

from vivisystem.client import VivisystemClient

POND_NAME = "Khor-pond"
VIVISYSTEM_URL = "ws://localhost:5000"

r = connect_to_redis()
fishStore = FishStore(r)
client = VivisystemClient(VIVISYSTEM_URL, POND_NAME)
pond = Pond("Khor-pond", fishStore, client)
pond.run()

# pond = Pond()
# pond.run()
