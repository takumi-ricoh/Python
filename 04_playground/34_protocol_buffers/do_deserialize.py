from person_pb2 import Person

person = Person()

#何も無い状態
print("befor")
print(person)
print("===================")

#デシリアライズ
person.ParseFromString(b'\n\x04Jhon\x10\xd2\t\x1a\x10jhon@example.com')
print("after")
print(person)