import xmlrpc.client
import socket
from pyrobase.parts import Bunch

class RtorrentClient():
    def __init__(
            self,
            socket:str=None,
        ):
        
        if socket:
            self.socket = socket

        self.torrent_files_cache = {}

        try:
            self.get_torrent_hashes()
        except Exception as e:
            print(f"Error connecting to rTorrent: {e}")
            exit(1)

    def torrent_fields(self):
        return ["d.name=", "d.hash=", "d.custom1=", 'd.incomplete=']
    
    def map_fields(self, torrents):
        field_map = {
            'd.hash=': 'hash',
            'd.name=': 'name',
            'd.custom1=': 'label',
            'd.incomplete=': 'incomplete'
        }

        fields = self.torrent_fields()

        mapped_torrents = []
        for torrent in torrents:
            mapped_torrent = {}
            for field, mapped_name in field_map.items():
                if field in fields:
                    index = fields.index(field)
                    mapped_torrent[mapped_name] = torrent[index]
            mapped_torrents.append(mapped_torrent)

        return mapped_torrents
    
    def get_multicall_params(self):
        common = ['', 'main']
        return common + self.torrent_fields()

    def get_current_speeds(self):
        speeds = {
            'download': self.scgi_request('get_down_rate'),
            'upload': self.scgi_request('get_up_rate')
        }
        return speeds
    
    def get_torrent_hashes(self):
        return self.scgi_request('download_list', ['', 'main'])[0][0]
    
    def get_torrent(self, hash:str):
        fields = self.torrent_fields()
        torrent = [None] * len(fields)
        for index, field in enumerate(fields):
            field = field.replace('=', '')
            if field == 'd.hash':
                torrent[index] = hash
                continue

            torrent[index] = self.scgi_request(field, hash)[0][0]

        return self.map_fields([torrent])[0]
    
    def get_torrents(self):
        raw_torrents = self.scgi_request('d.multicall2', *self.get_multicall_params())[0][0]
        return self.map_fields(raw_torrents)
    
    def get_torrent_messages(self, hash):
        failure_message = self.scgi_request('d.message', hash)
        return failure_message[0][0]
    
    def get_cached_torrent_files(self, torrent_hash):
        print(torrent_hash)
        if torrent_hash not in self.torrent_files_cache:
            file_names = self.get_torrent_files(torrent_hash)
            self.torrent_files_cache[torrent_hash] = file_names

        return self.torrent_files_cache[torrent_hash]
    
    def get_torrent_files(self, torrent_hash):
        files = self.scgi_request('d.multicall2', torrent_hash, '', 'f.path=')
        print(files)
        return [file[0] for file in files]

    def get_files_for_all_torrents(self):
        for torrent_hash in self.get_torrent_hashes():
            files = self.get_torrent_files(torrent_hash)
            self.torrent_files_cache[torrent_hash] = files
        return self.torrent_files_cache
    
    def set_label(self, torrent_hash, label):
        current_label = self.scgi_request('d.custom1', torrent_hash)[0][0]
        if current_label == label:
            return
        self.scgi_request('d.custom1.set', torrent_hash, label)

    def scgi_request(self, method, *params):
        if len(params) == 1 and not isinstance(params[0], list):
            request_params = (params[0],)
        else:
            request_params = params
        request = xmlrpc.client.dumps(request_params, method)
        header = f"CONTENT_LENGTH\x00{len(request)}\x00SCGI\x001\x00"
        request = f"{len(header)}:{header},{request}"

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self.socket)
        sock.sendall(request.encode())

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        sock.close()

        response_body = response.split(b'\n\n', 1)[1] if b'\n\n' in response else response

        header, xml_content = response.split(b'\r\n\r\n', 1)
        response_body = xml_content.decode('utf-8')

        return xmlrpc.client.loads(response_body)

    def scgi_multicall_request(self, calls):
        multicall_params = []
        for method_name, *params in calls:
            multicall_params.append({'methodName': method_name, 'params': params})
        
        request = xmlrpc.client.dumps((multicall_params,), 'system.multicall')
        header = f"CONTENT_LENGTH\x00{len(request)}\x00SCGI\x001\x00"
        request = f"{len(header)}:{header},{request}"

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self.socket)
        sock.sendall(request.encode())

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        sock.close()

        response_body = response.split(b'\r\n\r\n', 1)[1].decode('utf-8')

        return xmlrpc.client.loads(response_body)
