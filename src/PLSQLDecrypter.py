import random
verbose_output = False

def decrypt(encrypted):
    global verbose_output
    try:
        parts = [int(encrypted[i:i+4]) for i in range(0, len(encrypted), 4)]
        key = parts.pop(0)
        if verbose_output:
            print('Key: {0}'.format(key))
        decrypted = ''
        for i in range(len(parts)):
            n = parts[i]
            mask = (n - 1000) ^ (key + (i + 1)*10)
            c = chr(mask >> 4)
            if verbose_output:
                print('{0} : {1}'.format(n, c))
            decrypted += c
        if verbose_output:
            print('Decrypted: {0}'.format(decrypted))
            print('----')
        return decrypted
    except Exception as err:
        if verbose_output:
            print("Unexpected error:", err)
        return None

def encrypt(password, key=None):
    global verbose_output
    if key is None:
        key = random.randint(0, 999) + 2000
    else:
        key = min(2000, max(int(key), 2999))
    if verbose_output:
        print('Key: {0}'.format(key))
    encrypted = str(key)
    bs = bytes(password, 'utf-8')
    for i in range(len(bs)):
        b = bs[i]
        mask = b << 4
        n = (mask ^ (key + (i + 1)*10)) + 1000
        c = str(n).zfill(4)
        if verbose_output:
            print('{0} : {1}'.format(password[i], c))
        encrypted += c
    if verbose_output:
        print('Encrypted: {0}'.format(encrypted))
        print('----')
    return encrypted

class Connection:
    IsFolder = 0
    Number = None
    Parent = -1
    Username = None
    Database = None
    ConnectAs = None
    Edition = None
    Workspace = None
    AutoConnect = None
    ConnectionMatch = None
    Color = None
    Password = None
    IdentifiedExt = None

    def __init__(self, name):
        self.DisplayName = name

def parse(path):
    global verbose_output

    current_block = None
    current_connection = None
    connections = []
    current_connection_strings = []
    logon_history_strings = []

    try:
        with open(path) as prefs:
            for line in prefs:
                line = line.strip()
                if len(line) < 1:
                    pass
                elif line[0] == '[':
                    # new block
                    if current_connection:
                        connections.append(current_connection)
                        current_connection = None
                    current_block = line[1:-1]
                elif current_block == 'Connections':
                    parts = line.split('=')
                    if parts[0] == 'DisplayName':
                        # new connection
                        if current_connection:
                            connections.append(current_connection)
                        current_connection = Connection(parts[1])
                    else:
                        try:
                            setattr(current_connection,parts[0],parts[1])
                        except AttributeError:
                            pass
                elif current_block == 'CurrentConnections':
                    current_connection_strings.append(line)
                elif current_block == 'LogonHistory':
                    logon_history_strings.append(line)
    except FileNotFoundError:
        print("File '{}' does not exist".format(path))
    except OSError:
        print('File cannot be read')
    except:
        print('Error occurred accessing file')
    
    def get(n):
        return next(filter(lambda c: c.Number == str(n),  connections), None)
    
    org_verbose_output = verbose_output
    verbose_output = False
    if org_verbose_output:
        print('[Connections] ({0})'.format(len(list(filter(lambda c: c.IsFolder != '1', connections)))))
    for con in connections:
        if con.Password:
            result = decrypt(con.Password)
            if org_verbose_output:
                level = 0
                if con.Parent and con.Parent != '-1':
                    level = 1
                    parent = get(con.Parent)
                    while parent.Parent and parent.Parent != '-1':
                        level += 1
                        parent = get(parent.Parent)
                print('{0}"{1}": {2}/{3}@{4}'.format('  '*level, con.DisplayName, con.Username, result, con.Database))
            else:
                print('{0}/{1}@{2}'.format(con.Username,result,con.Database))
        elif org_verbose_output:
            if con.IsFolder == '1':
                print('Folder: {0}'.format(con.DisplayName))
    if org_verbose_output:
        print('')
        print('[CurrentConnections] ({0})'.format(len(current_connection_strings)))
    for line in current_connection_strings:
        result = decrypt(line).split(',')
        while len(result) < 3:
            result.append('')
        print('{0}/{1}@{2}'.format(result[0], result[1], result[2]))
    if org_verbose_output:
        print('')
        print('[LogonHistory] ({0})'.format(len(logon_history_strings)))
    for line in logon_history_strings:
        print(decrypt(line))
    verbose_output = org_verbose_output

def main():
    import argparse
    global verbose_output

    parser = argparse.ArgumentParser(description='PLSQL Developer Password Decrypter')
    parser.add_argument('input',                                help='File path or (encrypted) password with -d or -e flag')
    parser.add_argument('-d', '--decrypt', action='store_true', help="Signify input should be decrypted, rather than a file path")
    parser.add_argument('-e', '--encrypt', action='store_true', help="Signify input should be encrypted, rather than a file path")
    parser.add_argument('-k', '--key',                          help="Specify key for encrypting")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    args = parser.parse_args()
    
    if args.verbose:
        verbose_output = True

    if args.decrypt or args.encrypt:
        if args.encrypt:
            result = encrypt(args.input, args.key)
        else:
            result = decrypt(args.input)
        print(result)
    else:
        parse(args.input)

# Begin script
if __name__ == "__main__": main()