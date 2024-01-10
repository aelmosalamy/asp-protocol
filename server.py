import socketserver
import csv
import struct
import random
from caesarcipher import CaesarCipher
# Server implementation for the reliable, secure, comprehensive ASP protocol.
# Server supports ASP2 and ASP3. ASP1 is not supported.

supported_versions = [2, 3]
supported_methods = ['VERS', 'CAPS', 'ANIM', 'SOUN', 'ATOS']
_animals, _sounds, _data = [], [], {}

# returns (data, error)
def parse_packet(packet):
    if len(packet) < 12 or len(packet) > 32:
        return None, "ASPERR: Invalid packet size."

    header = packet[:12]
    body = packet[12:]

    return (header, body), None

def unpack_header(header):

    format_string = "!B3xB4s3x"
    
    # Unpack the packet using the format string
    unpacked_data = struct.unpack(format_string, header)
    # has version, key and data: (16, 53, b'6789')

    print(unpacked_data)
    # Extract individual fields
    version = (unpacked_data[0] >> 4) & 0xF
    key = unpacked_data[1]
    method = unpacked_data[2].decode('latin-1')

    # Create a dictionary to hold the unpacked data
    unpacked_header = {
        "version": version,
        "key": key,
        "method": method,
    }

    return unpacked_header

# returns error message on invalid data otherwise None
# decrypts the header in place
def validate_and_decrypt_header(data) :
    if data['version'] not in supported_versions:
        return f"ASPERR: Unsupported version '{data['version']}'."

    if data['key'] < 1 or data['key'] > 25:
        return f"ASPERR: Invalid key '{data['key']}'."

    data['method'] = CaesarCipher(data['method'], offset=data['key']).decoded

    if data['method'] not in supported_methods:
        return f"ASPERR: Unsupported method '{data['method']}'"

    return None

# reads animal-sound data from file
def load_atos():
    _animals = []
    _sounds = []
    _data = {}

    with open('asp_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for animal, sound in reader:
            _animals.append(animal)
            _sounds.append(sound)
            _data[animal] = sound

    return _animals, _sounds, _data


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        resp = b''
        
        # get all packet data
        self.data = self.request.recv(32).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        data, err = parse_packet(self.data)

        if err:
            return self.request.sendall(err.encode('latin-1'))

        _header, body = data
        header = unpack_header(_header)
        body = body.decode('latin-1').strip()

        # check if header is valid
        err = validate_and_decrypt_header(header)
        if err:
            return self.request.sendall(err.encode('latin-1'))

        # we have valid header and body now
        print(header, body)

        if header['method'] == 'VERS':
            resp = f'Server supports ASP versions {", ".join(map(str, supported_versions))}.'
        elif header['method'] == 'CAPS':
            resp = f'Server supports methods {", ".join(supported_methods)} as part of version {header["version"]}.'
        elif header['method'] == 'ANIM':
            if not body:
                resp = 'ASPERR: Invalid body.'
            else:
                animals = [a for a in _animals if a.startswith(body)]
                resp = f"Server has {len(animals)} animals starting with '{body}':\n{animals}"
        elif header['method'] == 'SOUN':
            if not body:
                resp = 'ASPERR: Invalid body.'
            else:
                sounds = [a for a in _sounds if a.startswith(body)]
                resp = f"Server has {len(sounds)} sounds starting with '{body}':\n{sounds}"
        elif header['method'] == 'ATOS':
            if not body:
                resp = 'ASPERR: Invalid body.'
            else:
                if body == 'Frog' and header['version'] == 3 and random.random() < 0.2:
                    resp = 'GlItCh iN ThE ASP mATRiX: RkxBR3t5b3VfbWFzdGVyM2RfcHJvdG9jb2w1fQo='
                elif body in _animals:
                    resp = f"'{body}' sound is {_ATOS[body]}"
                else:
                    resp = 'ASPERR: Animal not found.'

        # just send back the same data, but upper-cased
        self.request.sendall(CaesarCipher(resp,
                                          offset=header['key']).encoded.encode('latin-1'))


if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 9997

    # load animal sounds into a dict
    _animals, _sounds, _ATOS = load_atos()

    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
