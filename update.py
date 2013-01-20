import redis
import json 

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)


tle = json.dumps(["ISS (ZARYA)",
    "1 25544U 98067A   13019.24297745  .00019637  00000-0  32663-3 0   523",
    "2 25544  51.6466 128.2329 0013922 174.5549 270.6743 15.51955285811576"])


r.set("iss_tle", tle)
