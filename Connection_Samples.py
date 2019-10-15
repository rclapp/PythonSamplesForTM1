from TM1py import TM1Service


def find_gateway(target_server):

    kwargs = {'address': target_server.ip_address,
              'port': target_server.http_port_number,
              'ssl': target_server.using_ssl,
              'user': None,
              'password': None
              }

    try:
        response = TM1Service(**kwargs)
    except TM1pyException as e:
        response_headers = e.headers
        authenticate_header = response_headers.get("WWW-Authenticate", "No Gateway Found")
        if authenticate_header is not "No Gateway Found":
            gateway = authenticate_header.split("CAMPassport")[1].strip().split(",")[0]
            return gateway
        else:
            raise authenticate_header


def build_connection_parameters(admin_host, server_name, gateway=None, namespace=None):
    server_found = False
    kwargs = {}

    try:
        servers = TM1py.Utils.get_all_servers_from_adminhost(admin_host)
    except Exception as e:
        logger.error("Unable to connect to admin host: {}".format(e))
        raise e


    for s in servers:
        if s.name.lower() == server_name.lower():
            target_server = s
            server_found = True

    if not server_found:
        logger.error("Server: {} not found on admin host: {}".format(server_name, admin_host))
        raise Exception("Server: {} not found on admin host: {}".format(server_name, admin_host))

    kwargs = {'address': target_server.ip_address,
              'port': target_server.http_port_number,
              'ssl': target_server.using_ssl
              }

    elif gateway is not None and namespace is not None:

        kwargs.update({
            'gateway': gateway,
            'namespace': namespace,
            'user': None,
            'password': None
        })

    elif gateway is None and namespace is not None:

        try:
            gateway = find_gateway(target_server)

            kwargs.update({
                'gateway': gateway,
                'namespace': namespace,
                'user': None,
                'password': None
            })

        except Exception as e:
            raise e

    else:
        raise Exception("Missing Connection Information")