import addressbook_pb2
import sys

# 入力に応じてPersonのメッセージを作成
def PromptForAdress(person):
    person.id = int(input("ID番号を入れて"))
    person.name =  input("名前を入れて")

    email = input("メアドを入れて")

    if email != "":
        person.email = email

    while True:
        number = input("電話番号を入れて")
        if number == "":
            break

    phone_number = person.phones.add()
    phone_number.number = number

    type = input("これは携帯？家電話？仕事電話？")
    if type == "mobile":
        phone_number.type = addressbook_pb2.Person.PhoneType.MOBILE
    elif type == "home":
        phone_number.type = addressbook_pb2.Person.PhoneType.HOME
    elif type == "work":
        phone_number.type = addressbook_pb2.Person.PhoneType.WORK
    else:
        print("そんなタイプの電話はしらんのでデフォルトタイプにします")

# メインプロシージャ
# ファイルからすべてのアドレスブックを読む
# 入力から一人を追加し、ファイルに書く

#引数が2つでない場合は終了
if len(sys.argv) != 2:
    print("Usage:",sys.argv[0],"ADDRESS_BOOK_FILE")
    sys.exit(-1)

address_book = addressbook_pb2.AddressBook()

#既存のアドレスブックを読む
try:
    f = open(sys.argv[1],"rb")
    address_book.ParseFromString(f.read())
    f.close()
except IOError:
    print(sys.argv[1],"ファイルが開けません。新しいファイルを開きます")

#アドレス追加
PromptForAdress(address_book.people.add())

#ディスクに保存
f = open(sys.argv[1],"wb")
f.write(address_book.SerializeToString())
f.close()
