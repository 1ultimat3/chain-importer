import ijson.backends.yajl2 as ijson


def json_states(fd):
    parser = ijson.parse(fd)

    for prefix, event, value in parser:

        if event == 'start_map' and prefix and 'storage' not in prefix:
            # address based
            balance = ""
            nonce = ""
            address = ""

            # code based
            code = ""
            code_hash = ""
            code_storage_root = ""
            code_storage = {}

        elif event == 'end_map' and prefix and 'storage' not in prefix:
            if code:
                yield {
                    'address': address,
                    'nonce': nonce,
                    'balance': balance,
                    'code': code,
                    #'code_hash': code_hash,
                    'storage': code_storage,
                    #'storageRoot': code_storage_root
                }
            elif address:
                yield {
                    'address': address,
                    'nonce': nonce,
                    'balance': balance
                }

        elif '.' in prefix:
            if 'balance' in prefix:
                balance = value
                address = prefix.split('.')[1]
            elif 'nonce' in prefix:
                nonce = value
            elif 'code_hash' in prefix:
                code_hash = value
            elif prefix.endswith('code'):
                code = value
            elif 'storage_root' in prefix:
                code_storage_root = value
            elif 'storage' in prefix and event == 'string':
                _storage_address = prefix.split('.')[-1]
                code_storage[_storage_address] = value

