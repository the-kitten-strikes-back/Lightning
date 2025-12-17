import socket
def http_probe(target, port):

    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((target, port))
        req = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
        s.send(req.encode())
        data = s.recv(4096).decode(errors="ignore")
        s.close()
        return data
    except:
        return ""
def grab_banner(target, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((target, port))
        banner = s.recv(2048).decode(errors="ignore")
        s.close()
        return banner
    except:
        return ""
def smb_probe(target, port=445):
    try:
        from impacket.smbconnection import SMBConnection

        # '*' = negotiate best dialect automatically
        conn = SMBConnection(
            remoteName=target,
            remoteHost=target,
            sess_port=port,
            timeout=3
        )

        conn.login('', '')  # anonymous login attempt

        info = {
            "server_os": conn.getServerOS(),
            "server_name": conn.getServerName(),
            "domain": conn.getServerDomain(),
            "signing": conn.isSigningRequired(),
            "dialect": conn.getDialect()
        }

        conn.close()
        return info

    except Exception:
        return None
