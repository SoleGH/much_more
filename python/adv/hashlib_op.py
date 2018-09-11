import hashlib

def my_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


if __name__ == "__main__":
    print(my_md5("test md5"))