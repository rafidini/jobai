import time
from db.mongo import MongoDB
from setup.configuration import get_configuration

CONFIG = get_configuration(section='MongoDB')

connector = MongoDB(CONFIG)

result = connector.connect()

print(f"Connection has {'' if result else 'not '}been established! ({result})")

assert result

start = time.time()
frame = connector.get_dataframe(collection_name='job_offers')
end = time.time()
print(f"Time : {end - start}s")
print(frame.shape)
