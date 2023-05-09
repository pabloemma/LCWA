'''
Created on May 9, 2023

@author: klein
generates, encrypts and decrypts files
'''
# import required module
from cryptography.fernet import Fernet
import os.path
import sys

class MyCrypt(object):

    def __init__(self,keyfile,inputfile,encrypted_file = None, decrypted_file = None):

        pass

    def CreateKey(self,keyfile):
        '''only use if you haven't created a keyfile'''

        if not os.path.exists(keyfile):
            # key generation
            key = Fernet.generate_key()
 
            # string the key in a file
        
            with open(keyfile, 'wb') as filekey:
                filekey.write(key)
        else:
            print('this keyfile already exists, either delete it of give different name')
            sys.exit(0)

        return
    
    def EncryptFile(self,keyfile,inputfile,encrypted_file):
        # opening the key
        with open(keyfile, 'rb') as filekey:
            key = filekey.read()
 
        # using the generated key
        fernet = Fernet(key)
 
        # opening the original file to encrypt
        with open(inputfile, 'rb') as file:
            original = file.read()
     
        # encrypting the file
        encrypted = fernet.encrypt(original)
 
        # opening the file in write mode and
        # writing the encrypted data
        with open(encrypted_file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        return
    
    def DecryptFile(self,keyfile,encrypted_file,decrypted_file):

        with open(keyfile,'rb') as filekey:
            key = filekey.read()

        # using the key
        fernet = Fernet(key)
 
        # opening the encrypted file
        with open(encrypted_file, 'rb') as enc_file:
            encrypted = enc_file.read()
 
        # decrypting the file
        decrypted = fernet.decrypt(encrypted)
 
        # opening the file in write mode and
        # writing the decrypted data
        with open(decrypted_file, 'wb') as dec_file:
            dec_file.write(decrypted)
        
        return
    
if __name__ == '__main__':
    import os.path
    homedir         = os.path.expanduser('~')

    keyfile = homedir +'/git/LCWA/src/LCWAkey.txt'
    inputfile = homedir +'/git/LCWA/src/LCWA_a.txt'
    decrypted_file = homedir +'/git/LCWA/src/LCWA_ad.txt'
    encrypted_file = homedir +'/git/LCWA/src/LCWA_ae.txt'


    MCY = MyCrypt(keyfile,inputfile,decrypted_file=decrypted_file,encrypted_file=encrypted_file)
    MCY.CreateKey(keyfile)
    MCY.EncryptFile(keyfile,inputfile,encrypted_file)
    MCY.DecryptFile(keyfile,encrypted_file,decrypted_file)