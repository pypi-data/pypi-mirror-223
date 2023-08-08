# Cryptography App & Library w/ AES-256
##  Why ? ##
**Tired of juggling passwords and worrying about your private files?**
<br>**That's exactly why I cooked up this Python library. I craved a hassle-free solution to shield my personal content from prying eyes, and it hit me—maybe others are hunting for the same thing!**
## Overview ## 
![alt text](important/GUI.png)
The project incorporates an App & a library called **ashcrypt** : 

**App :** 
<br>Full-fledged application that integrates all the modules in the library merging them into a unified and powerful software solution for developers and for people with no programming knowledge whatsoever
<br>check [GUI](https://github.com/AshGw/ashcrypt#gui) header for more info.

**Library :** 
<br>A simple, secure, and developer-oriented library for performing encryption and decryption operations on data using the AES-256 (CBC) encryption algorithm.
<br>The core of the library is the module `crypt`
It offers cryptographic capabilities and security measures to safeguard
sensitive data,  providing a hassle-free experience when dealing with cryptographic libraries.
<br>View [Features](https://github.com/AshGw/ashcrypt#features) Header for more details.





### For Developers ###
The project uses `crypt` module to ensure secure data encryption and decryption for files and text while keeping it very easy and simple to use .
View the headers for [filecrypt](https://github.com/AshGw/ashcrypt#filecrypt) and [textcrypt](https://github.com/AshGw/ashcrypt#textcrypt) to learn more.


It also incorporates a database module which is there to allow key management & storage of classified content in a secure, 
safe and simple manner.

<br>The module has a simple straight forward approach for dealing with sqlite3 databases, even if you're not familiar with Python itself you can still use this module to run SQL queries with built in functions to perform various operations on a given database.<br>Check [database](https://github.com/AshGw/ashcrypt#database-1) header to learn more.

## Installation ##
### If you want to use it as a library ###
You can simply use **pip**
<br>First upgrade the package installer 
```bash
pip install --upgrade pip 
```
Then install the Library 
```bash
pip install ashcrypt
```
This will install the latest version of `ashcrypt`.
You can start using it in your code by importing its modules :

```python
from ashcrypt import crypt as ac
```
That's it.

### Whole repo installation 
Now if you want to get the whole repo with no manual configurations
<br>Run this command in the Terminal
```bash
curl -sSfL https://raw.githubusercontent.com/AshGw/ashcrypt/main/important/setup.sh | bash
```
This will run the commands in [setup.sh](important/setup.sh).
<br>It will clone & install all the dependencies needed on your machine and activate the development mode, inside the directory you're currently at.

**After the library is installed** 
<br>To run the GUI 
```shell
python -m ashcrypt.gui
```

## `crypt` Module ##
The `crypt.py` Module is a comprehensive collection of carefully designed functions and code modules that facilitate the performance and reliability for data encryption and decryption operations  while ensuring security and 
confidentiality.

<br>It uses primitives from the `cryptography` library with added security features while keeping it simple and highly flexible to provide a head-ache free solution for developers. 

<br>You can check [Features](https://github.com/AshGw/ashcrypt#features) tag below to learn more about the security features.

### Usage ##
1) Generate a key if you don't have one already
```python
mainkey = Enc.genkey()
```
2) Before encrypting or decrypting anything, first set the arguments you want to pass, you can have an encrypted message or a  decrypted message , and a mainkey to use.
<br>This will output a string type key (hex), you can choose to render your preferred key length too:
```python
mainkey = Enc.genkey(desired_bytes=64) # 512-bit long key
```
```python
mainkey = '6ce113be19e898c2b98df82b7fa8efb166928925fc05574a54eb1114c3410900'
```
The message can be of type str or bytes.
```python 
message = 'Hello There'  # str
message = b'Hello There' # bytes

# an encrypted message ( to decrypt ): 

message = 'ZEfikRiNQ4EE1y5E-Qn4gQbo8goVpWLPstqTlgWtoRq1CK_oeMz4oelCYNpM-NZyzSIKk7DazkAUO9HcZJzWWMXR6zqRjNTN-c1Q6vRWSkj1g20oL6JbzUvEJL3xvY2-Fye1simoOAr7YP5YHAnSYAAAADIA0juak_JYQnzXQ-apJ8azahvngigFrHRg142g7OqvfA=='

# or bytes encrypted message ( to decrypt ):

message = b'dG\xe2\x91\x18\x8dC\x81\x04\xd7.D\xf9\t\xf8\x81\x06\xe8\xf2\n\x15\xa5b\xcf\xb2\xda\x93\x96\x05\xad\xa1\x1a\xb5\x08\xaf\xe8x\xcc\xf8\xa1\xe9B`\xdaL\xf8\xd6r\xcd"\n\x93\xb0\xda\xce@\x14;\xd1\xdcd\x9c\xd6X\xc5\xd1\xeb:\x91\x8c\xd4\xcd\xf9\xcdP\xea\xf4VJH\xf5\x83m(/\xa2[\xcdK\xc4$\xbd\xf1\xbd\x8d\xbe\x17\'\xb5\xb2)\xa88\n\xfb`\xfeX\x1c\t\xd2`\x00\x00\x002\x00\xd2;\x9a\x93\xf2XB|\xd7C\xe6\xa9\'\xc6\xb3j\x1b\xe7\x82(\x05\xact`\xd7\x8d\xa0\xec\xea\xaf|'
```
3) Now pass the arguments accordingly. If you have a normal message and you try to decrypt it, an Exception will be raised so pass the arguments to the right classes. 
<br><br>So first create an instance of either the `Enc` or `Dec` class. 
<br>Here I chose to encrypt a message 
```python
a = Enc(message, mainkey)
```

4) Now you'd have to specify the output, you can encrypt to bytes or encrypt to URL-safe strings.
<br> Here I chose to encrypt to bytes
```python
output = a.encrypt(get_bytes=True)
```
you can also encrypt to a URL safe string
```python
output = a.encrypt()
```
<br> 
The same logic applies to the decryption process.

## Features ## 
- AES 256 CBC mode 
- Generates a randomly secure 256-bit main key 
- Derives the HMAC and the AES key from the mainkey using bcrypt's KDFs with a configurable number of iterations with :
    - Salt : Random 128 bit value is generated  each time and passed to the KDF to generate the AES key
    - Pepper : Random 128 bit value is generated  each time and passed to the KDF to generate the HMAC
- AES Key : 256 bit
- HMAC : 256 bit hashed using SHA256
- Generates a random 128 bit Initialization Vector (IV) each time for the Cipher
- PKCS7 message padding
### Other Features :
These focus on ease of use: 
- No need to manipulate the input to fit, it accepts strings or bytes you can pass them right away
- You can get a string or a bytes representation of either the encryption or the decryption result
- For the `crypt` module the key is flexible it must **at least** be 256-bit , so can go higher if you want ( although for `textcrypt` and `filecrypt` you have to use a 256 bit long key )
### Regarding KDFs
Note that bcrypt is intentionally slow and computationally expensive, enhancing protection against brute-force attacks. The number of iterations, including salt and pepper, increases derivation time to strike a balance between security and performance. Use a suitable value based on your machine's capabilities and desired security level.


<br>Im using 50 just to demonstrate the process and make it quick.
<br>The bare minimum is 50 ( which is secure enough ), the max is 100 000, choose somewhere in between.
<br>In my use case 50 takes around 0.5 secs while using the maximum number of iterations takes around 11 minutes to derive the keys and finish the cryptographic operations at hand.
<br>Check it by running this with various `iterations` values:

```python
import time
from ashcrypt import crypt

key = crypt.Enc.genkey()
t1 = time.perf_counter()
a = crypt.Enc('hello', key, iterations=50)
a.encrypt()
print(time.perf_counter() - t1)

t2 = time.perf_counter()
b = crypt.Enc('hello', key, iterations=200)
b.encrypt()
print(time.perf_counter() - t2)
```

## `filecrypt` ## 
If you want to encrypt a file :
1) Follow the steps above to set the key up.
2) Create an instance of the class CryptFile and pass 2 arguments, the first one being the target file and the second argument being the key :
```python
my_instance = CryptFile('target.txt', key)
```
```python
my_instance = CryptFile('test.db', key)
```
The file can be of anything : image`.png`, movie `.mp4`,`.sqlite`  etc..
<br>It doesn't have to just be of `.txt` extension ,can be of anything really.  
<br>**Note** : 
If the file is not in the working directory you can specify the whole path: 
<br>**For windows**
```python
target = CryptFile('C:\\Users\\offic\\MyProjects\\SomeOtherfolder\\myfile.txt',key) 
```
<br>**On Mac and Linux :**
```python
target = CryptFile('/User/Desktop/MyProjects/SomeOtherfolder/myfile.txt',key)
```
3) Apply either the `encrypt()` or `decrypt()` over that instance :
```python
my_instance = CryptFile('qrv10.png',key)
my_instance.encrypt()
```
you can apply `print()` on `my_instance.encrypt()`to check the result :
<br>If the output is 1 then the file has been successfully encrypted/decrypted + added/removed .crypt extension 
<br> Other than that it should raise an Exception with the specified Error.
```python
my_instance.encrypt()
```
```python
my_instance.decrypt()
```

That's it, if you follow the steps above then everything should work just fine.
## `textcrypt` ## 
Follow the same steps above, and keep in mind both accept either string type objects or bytes 
```python
my_instance = Crypt('Hello Wold !',key)
```
```python
my_instance.encrypt()[1]
```
```python
my_instance.decrypt()[1]
```
The result simply returns a tuple so index `[0]` is going to be the confirmation if it's `1` then it worked, else an exception will be raised.
<br>Index `[1]` contains the encrypted/decrypted content.

## `database` ##
To support efficient content management, I have integrated this database module to enable the storage and retrieval of encrypted content in a safe and secure manner using sqlite.

Ensuring that the encrypted data remains organized and readily accessible to anyone with the right key. Any content going in must be encrypted with a key that you must keep secured.


### Usage ## 
In this module I'm providing built-in functions to make it easier to perform usual queries over Sqlite tables , by default it creates a table `Classified` with two default columns :

**content** : This can be a single character or a whole movie in binary, that depends on your specific needs.

**key** : This key column wasn't indeed meant to store a key itself but rather store a reference to the actual key.
1) Create a connection to the database :
```python
conn = Database('test.db')
```
This would automatically set the default table name to `Classifed`, if no arguments are passed then all class methods would be using the default table name , if you want to set your own default table name instead of `Classified` you can pass your table name as the second argument : 
```python
conn = Database('test.db','mytable')
```
2) create/add the table to the database :
```python
conn.addtable()
```
Add the default table that's been set to the database,  if you want to pass an argument to the function that would create another table of your choice

3) Set a reference to the key not the key itself : 
```python
 key = '#5482A'
```
4) Use the connection to perform various tasks <br>
The content can be anything post encryption bytes or string format
```python
content='Some Encrypted Content'
conn.insert(content=content,key='#1E89JO', optional_table_name=None)
```
If the optional table name is `None` then it will insert data into the default table , else it would insert data into the table you specify


5) You can check the tables you have , it returns a generator object, yields the result of each element so you must run a for loop over it
```python
for e in conn.show_tables():
        print(e)
```
You can check the current size of the database using the size property method 
```python
print(conn.size) # Size of the Database in MB 
```

6) Check the module itself so you can run through all the available methods.
<br>The available methods can perform usual operations like insertion, deletion , updating the database and more..
<br>Use your editor and hover over the target function and it will fetch the docstrings for it.


7) to run more complex queries I've dedicated a query function that takes in `*queries` and returns the result fetched 
```python
query = 'SELECT COUNT(*) AS cc ,content FROM Classified WHERE key = "#5482A" ORDER BY cc DESC '
print(conn.query(query))
```
The result fetched should look like this : 
 ```python
[{'query 0': ['SUCCESS', [(1, 'some encrypted content of bytes or strings')]]}]
```
If some error has occurred while querying like : 
```python
query = 'SELECT COUNT(*) AS cc ,content FROM DoesntExist WHERE key = "#5482A" ORDER BY cc DESC '
```
The result fetched should look similar to this : 
```python
[{'query 0': ('FAILURE', 'no such table: DoesntExist')}]
```
That's it so simple !


## `GUI` ##
The GUI as mentioned above is a fully functional application , you can use it to enc/dec files , text , keep track of files by storing them on demand in the main database , also on demand it can keep track of the keys used for cryptographic operations.
### Usage ###
1) Set the main key up. If you don't have one , press on the button `generate` to generate a secure safe key ready for use. Then insert it in the `MAINKEY` entry
2) Now you're able to encrypt files or text (text is limited to 200 characters max)
####  Text : 
- You can insert some text in the entry right below the `TEXT ENCRYPTION` label.<br>The given text will be encrypted and you can choose if you want to have that text displayed as a qr code, a qr image will pop on the screen and you'll be able to scan it using your phone.
- Insert some encrypted text below the `TEXT DECRYPTION` label.<br>The given text will be decrypted and you'd have the option to display the "plaintext" as a qr code to be scanned by other devices.
<br>If the text cannot be decrypted it will display itself , so you might as well use this to display the key you're using as a qr code 

#### Files
- Under the `FILE PATH` label enter the file name (if it's in the current working directory) or submit the whole file path , the file can be of any type, click on `ENCRYPT FILE` button to encrypt the given file , if the encryption turns out to be successful , you'll see a success message along with a `added .crypt extention to the file` message. If the encryption wasn't successful you'll see an error message specifying the problem.<br>Note that you cannot re-encrypt a file that  has `.crypt` as extention.
- The file name should be changed by now to `filename + '.crypt'` , if the file has .crypt extension you can go ahead and decrypt it , if the same key is used for both enc/dec operations then the result should be `success` + `removed .crypt extention` from the file.
#### Database
- Now you have some encrypted/decrypted files but you want to keep them stored somewhere safe, this is where the main database comes in , where you need to store your files + their content + reference to the key used for their encryption/decryption. you can specify your database by :
1) Specifying the actual path where you want your database to be 
2) Give it a name, it must be a valid file name that ends with `.db` .<br>
If the database doesn't exist then a database with the name you've given will be created and automatically connected to.<br>If the given database already exists then it will automatically connect.
3) Did I mention the keys' database ? if you give your database a name it will also create the keys database with the same name as the database you chose plus `Keys` added to the name. This database holds the actual keys and the reference to these keys.
<br>The only piece of data that these two separate databases have in common is the key reference values.  

   
**Info**: 
<br>Both databases have the same table called `Classified` that has 4 columns <br>`ID` which is auto generated & incremented for each piece of data that gets inserted<br>
`Name` that holds the filename in both db's , although for the keys database if you haven't specified any file to operate on while selecting different keys, then all these inserted keys will be tagged with: `STANDALONE` 
<br>`Content` for the main db, this holds the entire content of the given file whereas for the keys db that holds the actual 256 bit encryption key.
<br>`Key` for  both db's, this holds the `KeyRef` A.K.A key reference value
#### Usage 
The buttons are self-explanatory so do what you see fit. The result of any task related to the databases is displayed on `DATABASE OUTPUT CONSOLE` 
<br>You can run a query anytime by writing a query ( raw sqlite query ) and clicking on `query` button , the result will be displayed to an `output.json` file that auto-deletes when you exit the app.
<br>Just click buttons and check the result in the output console, it will guide you through the process.

<br>To run the GUI anywhere
```shell
python -m ashcrypt.gui
```


## License ##
This project is licensed under the [MIT LICENSE](https://github.com/AshGw/ashcrypt/blob/main/LICENSE).
## Acknowledgments ##
This cryptographic scheme is inspired by secure cryptographic practices and various open-source implementations.

