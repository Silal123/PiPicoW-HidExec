import socketpool
import adafruit_httpserver
import struct
import adafruit_logging as logging

class CaptivePortalDns():
    def __init__(self, socket_pool: socketpool.SocketPool, http_server: adafruit_httpserver.Server, logger: logging.Logger, self_ip):
        self.socket_pool = socket_pool
        self.logger = logger
        self.running = False
        self.self_ip = self_ip
        '''
        @server.route("/generate_204")  # Android erwartet eine leere Antwort
@server.route("/gen_204")
def android_captive(request):
    return Response(request, "", status=adafruit_httpserver.NO_CONTENT_204)


@server.route("/hotspot-detect.html")  # Apple Captive Portal
@server.route("/ncsi.txt")  # Windows Captive Portal
@server.route("/connecttest.txt")  # Windows Captive Portal
def captive_portal(request: Request):
    return FileResponse(request, filename='index.html', root_path='/www')
        '''

        self.ALLOWED_DOMAINS = [
            b"connectivitycheck.gstatic.com",  # Android
            b"detectportal.firefox.com",  # Firefox
            b"www.msftncsi.com",  # Windows
            b"captive.apple.com",  # Apple
            b"clients3.google.com",
            b"clients4.google.com",
            b"clients5.google.com",
        ]
        pass

    def run(self):
        self.dns_socket = self.socket_pool.socket(self.socket_pool.AF_INET, self.socket_pool.SOCK_DGRAM)
        self.dns_socket.bind(('0.0.0.0', 53))
        self.logger.info("DNS-Server running!")
        self.running = True

    def loop(self):
        if not self.running:
            return
        try:
            # Create a buffer to hold the incoming data
            buffer = bytearray(512)  # 512 bytes buffer for DNS requests
            addr = None  # Initialize remote address variable
            
            # Use recvfrom_into to receive data and remote address
            num_bytes, addr = self.dns_socket.recvfrom_into(buffer)
            if num_bytes == 0:
                return  # No data received
            
            # Domain extraction
            domain_parts = []
            i = 12  # DNS header length
            while True:
                length = buffer[i]
                if length == 0:
                    break
                domain_parts.append(buffer[i + 1 : i + 1 + length])
                i += length + 1
            domain_name = b".".join(domain_parts)

            # Process allowed domains
            if domain_name in self.ALLOWED_DOMAINS:
                self.logger.info(f"DNS Request for {domain_name.decode()} -> {self.self_ip} More data: {addr}, {domain_parts}, {num_bytes}")
                self.dns_socket.sendto(self.dns_response(buffer), addr)

        except Exception as e:
            self.logger.error(f"DNS-Server Error: {e}")
            pass


    def dns_response(self, data):
        transaction_id = data[:2]  # Transaktions-ID
        flags = b"\x81\x80"  # Antwort-Flags
        qdcount = data[4:6]  # Anzahl der Anfragen
        ancount = qdcount  # Anzahl der Antworten (gleich)
        nscount = b"\x00\x00"  # Keine zusätzlichen Antworten
        arcount = b"\x00\x00"  # Keine zusätzlichen Einträge
        #question = data[12:]  # Frage aus dem Paket extrahieren

        q_name_end = 12  # Start of the question
        while data[q_name_end] != 0:
            q_name_end += data[q_name_end] + 1
        q_name_end += 5 # Advance past type and class fields
        question = data[12:q_name_end] # Extract the question

        ip_parts = [int(part) for part in str(self.self_ip).split(".")]

        self.logger.debug(f"Ip parts: {ip_parts}")

        # Antwort erstellen (besteht aus Header + Frage + Antwort)
        response = (
            transaction_id + 
            flags + 
            qdcount + 
            ancount + 
            nscount + 
            arcount + 
            question +
            b"\xc0\x0c" +  # Komprimierter Name
            b"\x00\x01" +  # Typ A
            b"\x00\x01" +  # Klasse IN
            b"\x00\x00\x00\x3c" +  # TTL = 60 Sekunden
            b"\x00\x04" +  # Länge der IP-Adresse
            struct.pack("!BBBB", *ip_parts)  # Antwort-IP
        )
        return response
