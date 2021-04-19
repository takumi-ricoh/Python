set SRC_DIR="C:\Users\p000495138\OneDrive - Ricoh\Share\my_github\02_Python\04_playground\34_protocol_buffers"
set DST_DIR="C:\Users\p000495138\OneDrive - Ricoh\Share\my_github\02_Python\04_playground\34_protocol_buffers"
::set file = "addressbook.proto"
set file="person.proto"

protoc -I=%SRC_DIR% --python_out=%DST_DIR% %SRC_DIR%/%file%

pause