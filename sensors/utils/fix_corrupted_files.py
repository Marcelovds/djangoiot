

# check for NULL bytes in the file
def is_corrupted(file_path):
    file = open(file_path, 'rb')
    data = file.read()
    position = data.find(b'\x00')
    file.close()
    return position != -1


# remove any NULL bytes from the file if any
def fix_corrupted_file(file_path):
    if not is_corrupted(file_path):
        return

    fi = open(file_path, 'rb')
    data = fi.read()
    fi.close()
    fo = open(file_path, 'wb')
    fo.write(data.replace(b'\x00', b''))
    fo.close()
    print('file ' + file_path + ' had NULL bytes and has been fixed')
