import http.client
import socket

def add_port_forwarding(target_ip, gateway_ip, external_port, internal_port, protocol):
    # If target_ip is empty, use the local IP of the machine running the program
    if not target_ip:
        target_ip = socket.gethostbyname(socket.gethostname())

    # Create the SOAP message with the required parameters
    soap_message = f"""
        <?xml version="1.0"?>
        <s:Envelope
            xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
            s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:AddPortMapping xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1">
                    <NewRemoteHost></NewRemoteHost>
                    <NewExternalPort>{external_port}</NewExternalPort>
                    <NewProtocol>{protocol}</NewProtocol>
                    <NewInternalPort>{internal_port}</NewInternalPort>
                    <NewInternalClient>{target_ip}</NewInternalClient>
                    <NewEnabled>1</NewEnabled>
                    <NewPortMappingDescription>UPnP Port Forwarding</NewPortMappingDescription>
                    <NewLeaseDuration>0</NewLeaseDuration>
                </u:AddPortMapping>
            </s:Body>
        </s:Envelope>
    """

    # Define the required HTTP headers for the SOAP message
    headers = {
        'Content-Type': 'text/xml',
        'SOAPAction': '"urn:schemas-upnp-org:service:WANIPConnection:1#AddPortMapping"',
    }

    # Establish an HTTP connection with the UPnP device and send the SOAP message
    conn = http.client.HTTPConnection(gateway_ip, timeout=10)
    conn.request('POST', '/upnp/control/WANIPConn1', soap_message, headers)
    response = conn.getresponse()

    conn.close()

    # Check the response to determine if the port forwarding was added
    if response.status == 200:
        return True
    else:
        return False
