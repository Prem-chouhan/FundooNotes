import redis

redis_host = '127.0.0.1'
redis_port = 6379
redis_password = "admin@123"


def hello_redis():
    try:
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.StrictRedis(host='127.0.0.1', port='6379', password='admin@123', decode_responses=True)

        # step 4: Set the hello message in Redis
        r.set("msg:hello", "Hello Redis!!!")
        # step 5: Retrieve the hello message from Redis
        msg = r.get("msg:hello")
        print(msg)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    hello_redis()
