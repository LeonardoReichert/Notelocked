#!/usr/bin/env python3


"""

This file is part of Notelocked.
Copyright (C) 2022  Leonardo A. Reichert

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
#you can see the full license at: "LICENSE" file

#https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

# Contact: leoreichert5000@gmail.com


# cip_fileformat or cipher module of program


#"text locked"(ltxt) file format and its encryption used


#we need: "pip install pycryptodome"
#or see https://www.pycryptodome.org/src/installation


from Crypto.Cipher import AES;
from Crypto.Util.Padding import pad, unpad;
from Crypto.Random import get_random_bytes;
from hashlib import algorithms_available;
from hashlib import new as newSha;
from sys import getdefaultencoding;
from sys import version_info as py_version;



if py_version[0] < 3:
    #Ok, I couldn't accept the way to encode bytes in Python 2
    raise Exception("Need Python >= 3");



SHA_NAME = "sha256"; #max 19 chars

#SHA validator :
hashLenght = 64


#file descriptors:
ext = "ltxt";
format_name = "Locked Text";


VECTOR_LENGTH = 16;

#default value used by the system encode o decode local text plain:
default_encoding = getdefaultencoding();


####################
### HEADERS FILE ###

idFileIdentifier = b"_Locked_"*10; #80 unique bytes
idFileVersion = b"0.5";
idFileSHA_NAME = SHA_NAME.encode();
idFileModeCipher = b"MODE_CBC";



MIN_PASSWORD = 12;
MAX_PASSWORD = 32;

assert MAX_PASSWORD % 16 == 0; #mode cbc x16


############
## Errors ##

ERR_SUCCES = 0;
ERR_PASSWORD_INCORRECT = -1;
ERR_FILE_INCORRECT = -2;
ERR_FILE_CORRUPT = -3;
ERR_FILE_OPEN = -4; #cannot open
ERR_NEED_RETRY = -5; #an error ocurred
ERR_FILE_VERSION = -6; #file version
ERR_NOALGO_HASH = -7; #no have algorithm sha


def getMessageErrorString(err):
    if err == ERR_PASSWORD_INCORRECT:
        return "Password incorrect";

    elif err == ERR_FILE_INCORRECT:
        return "File incorrect, not have the correct identifier";

    elif err == ERR_FILE_CORRUPT:
        return "File corrupt can't open";

    elif err == ERR_FILE_OPEN:
        return "File cannot open";

    elif err == ERR_NEED_RETRY:
        return "An error ocurred, please retry";

    elif err == ERR_FILE_VERSION:
        return "Error: File version incorrect";

    elif err == ERR_NOALGO_HASH: #no have algorithm sha
        return "Error: hashlib no have algorithm for the hash";

    return "Error unknown";


def existsAlgoHash(nameshafunc):
    """ we have algorithm sha's in hashlib ? """
    if nameshafunc in algorithms_available:
        return True;
    return False;


if not existsAlgoHash(SHA_NAME):
    #no have algorithm on hashlib
    raise Exception( getMessageErrorString(ERR_NOALGO_HASH) +": " + SHA_NAME );


def encrypt(sbytes, password, iv=None):
    #CBC: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
    #sbytes is str or bytes
    
    if type(sbytes) == str:
        sbytes = sbytes.encode(errors="replace");
    
    sbytes = pad(sbytes, VECTOR_LENGTH, "iso7816"); #fill with 0x80.. 0 ...

    if len(password)%VECTOR_LENGTH:
        password = pad(password, VECTOR_LENGTH, "iso7816"); #+0x80.. 0 ...

    if not iv:
        iv = get_random_bytes(VECTOR_LENGTH); #happens anyway
        
    cip = AES.new(password, AES.MODE_CBC, iv);
    return (cip.iv, cip.encrypt(sbytes));


def decrypt(iv, block, password):
    
    if len(password)%VECTOR_LENGTH:
        password = pad(password, VECTOR_LENGTH, "iso7816"); #+0x80.. 0 ...
    
    cip = AES.new(password, AES.MODE_CBC, iv);
    des = cip.decrypt(block);

    try:
        return unpad(des, VECTOR_LENGTH, "iso7816");
    except:
        return des;


def save_filename(filename, plain_text, password, text_encoding=default_encoding):

    """
    paded used: iso7816
             b'asd\x80\x00\x00..\x00'
     
    save file bytes as:
        + unique identifier header      80 unique bytes
        + identifier file version
        + sha func name                 (usually "sha256")
        + hash of of password
        + name mode encryption          (usually mode_cbc)
        + encoding used                 (usually "utf-8", paded to 25 bytes)
        + hash of password+encryption
        + random vector generated       (usually 16 bytes)

    return:
    code == 0 ( Succes ),
        getMessageErrorString(code)
    
    """
    
    if type(plain_text) == str:
        plain_text = plain_text.encode(text_encoding, errors="replace");
    
    if type(password) == str:
        password = password.encode();
    
    try:

        text_encoding = text_encoding.encode()

        fp = open(filename, "wb");

        hashPassword = newSha(SHA_NAME, password).hexdigest().encode();

        ######################################
        
        vector_random, encrypted = encrypt(plain_text, password);

        #fill with a hash for cheeck original content sha256(password + plain_text)
        hash_content = newSha(SHA_NAME, password+encrypted).hexdigest().encode();
        assert len(hash_content) == 64;
        
        fp.write(idFileIdentifier+b"\n") #unique header file identificator
        fp.write(idFileVersion+b"\n");
        fp.write(idFileSHA_NAME+b"\n");
        fp.write(hashPassword+b"\n");
        fp.write(idFileModeCipher+b"\n");
        fp.write(text_encoding+b"\n");
        fp.write(hash_content+b"\n");
        fp.write(vector_random.hex().encode()+b"\n");
        
        #double line separator
        fp.write(b"\n"+encrypted);

        fp.close();

    except Exception as msg:
        #print("msg", msg);
        return ERR_NEED_RETRY;

    return ERR_SUCCES;


def get_hash_saved(filename):

    """
    return: (int: error code,
                    code == 0 ( Succes ),
                    getMessageErrorString(code)
                    
             str: name sha function (usually sha256),
             str: hash representation of the user key on file)
    """

    try:
        file = open(filename, "rb");
    except:
        return (ERR_FILE_OPEN, "", "");

    #no have the unique identifier of file?
    if file.read(len(idFileIdentifier)+1) != idFileIdentifier+b"\n":
        file.close();
        return (ERR_FILE_INCORRECT, "", "");

    metadata = b"";
    while not metadata.endswith(b"\n\n"):
        bchar = file.read(1);
        metadata += bchar;
        if not bchar:
            file.close();
            return (ERR_FILE_CORRUPT, "", "");
    
    metadata = metadata.replace(b"\n\n", b""); #replace at the end
    fversion = "";
    try:
        fversion, nameSha, hashPassword, metadata = metadata.split(b"\n", 3);
        assert len(hashPassword) == hashLenght;
    except:
        file.close();
        if fversion and fversion != idFileVersion:
            return (ERR_FILE_VERSION, "", ""); #version wrong ?
        return (ERR_FILE_CORRUPT, "", "");

    return (ERR_SUCCES, nameSha.decode(), hashPassword.decode());


def load_filename(filename, password):

    """
        return [int: error code,
                string plain text: decrypted file if password is correct,
                bool: check True if content is original, calculated by the hash of
                                                            (password+encrypted)
                ]
    """

    try:
        file = open(filename, "rb");
    except:
        return (ERR_FILE_OPEN, "", 0);

    #no have the unique identifier of file?
    if file.read(len(idFileIdentifier)+1) != idFileIdentifier+b"\n":
        file.close();
        return (ERR_FILE_INCORRECT, "", 0);

    metadata = b"";
    while not metadata.endswith(b"\n\n"):
        bchar = file.read(1);
        metadata += bchar;
        if not bchar:
            file.close();
            return (ERR_FILE_CORRUPT, "", 0);
    
    metadata = metadata.replace(b"\n\n", b""); #replace at the end
    try:
        fver,nameSha,hashPassword,mode,enc,hashContent,vector = metadata.split(b"\n");
        assert len(hashPassword) == hashLenght;
        assert len(hashContent) == hashLenght;
        vector = b"".fromhex(vector.decode());
        assert len(vector) == VECTOR_LENGTH;
    except (AssertionError, ValueError):
        file.close();
        if fver != idFileVersion:
            return (ERR_FILE_VERSION, "", 0); #version wrong ?
        return (ERR_FILE_CORRUPT, "", 0);

    nameSha = nameSha.decode();
    if not existsAlgoHash(nameSha):
        file.close();
        return (ERR_NOALGO_HASH, "", 0);

    password = password.encode();

    hashPassword = hashPassword.decode();
    if newSha(nameSha, password).hexdigest() != hashPassword:
        file.close();
        return (ERR_PASSWORD_INCORRECT, "", 0);

    hashContent = hashContent.decode();
    encoding = enc.decode();

    encrypted = file.read();

    isOriginal = newSha(nameSha, password+encrypted).hexdigest() == hashContent;

    try:
        plainText = decrypt(vector, encrypted, password);
        plainText = plainText.decode(encoding);
    except:
        return (ERR_FILE_CORRUPT, "", 0);

    return (ERR_SUCCES, plainText, isOriginal);



'''
def _lot_updater(from_folder, new_foldername, passwords):
    """
    Dev function, this is used when I need to update the structure of the format file
      First I update the save file function,
      and after update the loader function
    Basically it has helped me to update my files
     when I have been changing things in the file format.
    """
    from glob import glob;
    from os.path import basename, splitext, exists;
    from os import mkdir, getcwd;

    print("The current dir is: %s" % getcwd());
    print("Workin in folder: %s" % from_folder);

    if not exists(new_foldername):
        print("The directory %s not exits, it will created..", end="");
        mkdir(new_foldername);
        print("ok");

    new_foldername = new_foldername.removesuffix("/").removesuffix("\\");

    print("Save new files in: %s\n" % new_foldername);

    filenames = glob("%s/*.*" % from_folder);

    print("%d files" % len(filenames))


    toUpdate = [];

    for fname in filenames:
        isOk = False;
        errcode, nameSha, theHash = get_hash_saved(fname);
        if errcode:
            print(" Error %d " % errcode, getMessageErrorString(errcode), fname);
            continue;

        for psw in passwords:
            if newSha(nameSha, psw.encode("utf-8")).hexdigest() == theHash:
                #is password correct:
                isOk = True;
                break;

        if not isOk:
            print(fname, "  \tneed other password");
            continue;

        print(fname, "  \tpassword correcta\t", psw);

        toUpdate.append((fname, psw));


    if not toUpdate:
        return;

    if input("Enter \"y\" for continue with update all files to a new version: ").upper() != "Y":
        return;
        
    print("\n ** updating to new version, %d files ** \n" % len(toUpdate));

    toTest = [];
    
    for fname, psw in toUpdate:
        errcode, plain_text, enc, isOriginal = load_filename(fname, psw);
        if errcode:
            print("Error of file %s:" % fname, getMessageErrorString(errcode));
            continue;

        print("old ingetegrity:", "yes" if isOriginal else "not",
              end="");

        new_filename = new_foldername+"/"+basename(fname);

        new_filename = splitext(new_filename)[0] + "." + ext;

        errcode = save_filename(new_filename, plain_text, psw, enc);
        if not errcode:
            print(" Success, saved on %s" % new_filename);
        else:
            print(" Error %d " % errcode, getMessageErrorString(errcode), new_filename);
            continue;

        toTest.append((fname, psw));

    print("\n ** testing new %d files ** \n" % len(toTest));

    for fname, psw in toTest:
        load_filename(fname, psw);
        print("ok:", fname);
        
    input("end - pause");


_lot_updater("saves/V3", "saves/V4/",
["pswordtest123",
],
);
'''





