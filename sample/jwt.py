import time

# from time import timestamp

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

timestamp = time.time()


def genTokenSeq(expires):
    s = Serializer(secret_key="123456789", salt="123456789", expires_in=expires)
    return s.dumps({"user_id": "1614010432", "user_role": "1", "iat": timestamp})


print(genTokenSeq(10000), timestamp)

token = genTokenSeq(10000)

s1 = Serializer(secret_key="123456789", salt="123456789")
print(s1.loads(token))
