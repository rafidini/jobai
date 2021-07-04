import json
import time
import pandas as pd
from db.mongo import MongoDB, df_to_formatted_json
from setup.configuration import get_configuration

# Connection
CONFIG = get_configuration(section='MongoDB')
connector = MongoDB(CONFIG)
result = connector.connect()
print(f"Connection has {'' if result else 'not '}been established! ({result})")
assert result

# Operation
start = time.time()
data = pd.read_csv('data/jobs_before.csv').drop_duplicates('link').drop(columns='_id')
jobs = []
N = 100
print("DataFrame dimensions:", data.shape, f"{round(time.time() - start, 2)}s")

for i in range(0,N):
    start = time.time()
    index_inf = 1 + (i * data.shape[0])
    index_sup = (i+1) * data.shape[0]
    index_inf = index_inf-1 if i == 0 else index_inf
    sub_jobs = data.iloc[index_inf:index_sup].pipe(df_to_formatted_json)
    jobs = jobs + sub_jobs

end = time.time()
print(f"Time : {round(end - start, 2)}s")
print(f"{len(jobs)} == {data.shape[0]} ? = {len(jobs) == data.shape[0]}")

for i in range(len(jobs)):
    r = connector.insert(item=jobs[i])
    print(f"Progress {round((i+1)/len(jobs) * 100)}% {r}")
