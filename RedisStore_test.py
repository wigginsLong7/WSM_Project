from RedisStore import RedisStore

rs = RedisStore('localhost', 6379, 0)
if rs.store('someKey', 'someValue'):
    print("Successfully store!")
else:
    print("Failed to store")

key = 'someKey'
val = rs.fetch(key)
print(key + ":" + val)

newVal = 'newValue'
print("Change the value of " + key)
if rs.change(key, newVal):
    print("Successfully change!")
else:
    print("Failed to change")

val = rs.fetch(key)
print(key + ":" + val)

print("Reset the whole db")
rs.reset()
val = rs.fetch(key)
print(val)
