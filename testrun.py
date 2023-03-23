from Pond import Pond

from FishStore import FishStore, connect_to_redis

r = connect_to_redis()
fishStore = FishStore(r)

pond = Pond("Khor-pond", fishStore)
pond.run()

# pond = Pond()
# pond.run()
