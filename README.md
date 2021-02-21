# PLSQLDevPass

_Stored Password Decryption for [Allround Automations'](http://www.allroundautomations.com/plsqldev.html) PL/SQL Developer._

## Install

### Download

``` bash
git clone https://github.com/taylor8294/PLSQLDevPass.git
cd PLSQLDevPass
python src/PLSQLDevPass.py -h
```

## Usage

Many thanks to Adam Caudill whose insightful [blog post](https://adamcaudill.com/2016/02/02/plsql-developer-nonexistent-encryption/) is the basis for this library.

PL/SQL Developer stores saved passwords in an INI-like file typically located in `C:\Users\<username>\AppData\Roaming\PLSQL Developer\Preferences\<username>\user.prefs`. The passwords are not stored in plain text, rather they are 'encrypted' with a simple xor and bitshift routine.

If you pass the path to your preferences file to the python script (or the windows executable from the releases page), it will decrypt all the database connection strings (usernames and passwords) that it finds in the file and print them to the console. It can also encrypt or decrypt a given string.

```
PLSQLDevPass>python src/PLSQLDecrypter.py -h
usage: PLSQLDecrypter.py [-h] [-d] [-e] [-k KEY] [-v] input

PLSQL Developer Password Decrypter

positional arguments:
  input              File path or (encrypted) password with -d or -e flag

optional arguments:
  -h, --help         show this help message and exit
  -d, --decrypt      Signify input should be decrypted, rather than a file path
  -e, --encrypt      Signify input should be encrypted, rather than a file path
  -k KEY, --key KEY  Specify key for encrypting
  -v, --verbose      Enable verbose output

PLSQLDevPass>python src/PLSQLDecrypter.py -v src/sample.prefs
[Connections] (4)
Folder: Folder1
  "Connection1-1": username11/password11@domain/db
  "Connection1-2": username12/password12@domain/db
Folder: Folder2
  "Connection2-1": username21/password21@domain/db
  "Connection2-2": username22/password22@domain/db

[CurrentConnections] (4)
username11/password11@domain/db
username12/password12@domain/db
username21/password21@domain/db
username22/password22@domain/db

[LogonHistory] (4)
username11/@domain/db
username12/@domain/db
username21/@domain/db
username22/@domain/db

PLSQLDevPass>python src/PLSQLDecrypter.py -k 2000 -e password
200012181500122212004954483648944680

PLSQLDevPass>python src/PLSQLDecrypter.py -d 200012181500122212004954483648944680
password

PLSQLDevPass>
```

## License

### Commercial license

If you want to use PLSQLDevPass as part of a commercial site, tool, project, or application, the Commercial license is the appropriate license. With this option, your source code is kept proprietary. To acquire a PLSQLDevPass Commercial License please [contact me](https://www.taylrr.co.uk/).

### Open source license

If you are creating an open source application under a license compatible with the [GNU GPL license v3](https://www.gnu.org/licenses/gpl-3.0.html), you may use PLSQLDevPass under the terms of the GPLv3.

---

By [Taylor8294 🌈🐻](https://www.taylrr.co.uk/)
