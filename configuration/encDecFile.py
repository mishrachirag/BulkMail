from cryptography.fernet import Fernet


def EncryptPass(Password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    HPass = fernet.encrypt(Password.encode()).decode('utf-8')
    length = len(HPass)//2
    leftPart,rightPart = HPass[:length],HPass[length:]
    MainPass = f"{leftPart}/=/{key.decode('utf-8')}/=/{rightPart}"
    return MainPass


def DecryptPass(HashPass):
    data = HashPass.split("/=/")
    leftPart,key,rightPart = data[0],data[1],data[2]
    fernet = Fernet(key)
    data = (leftPart+rightPart).encode()
    MainPass = fernet.decrypt(data).decode('utf-8')
    return MainPass