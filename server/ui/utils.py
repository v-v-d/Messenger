from PyQt5.QtGui import QStandardItemModel, QStandardItem

from db.utils import get_active_sessions, get_clients

from db.models import ClientSession


def get_connections_model():
    active_sessions = get_active_sessions()
    connections_model = QStandardItemModel()
    connections_model.setHorizontalHeaderLabels([
        'Client', 'IP address', 'Port', 'Created'
    ])

    for session in active_sessions:
        client = session.client.name
        addr = session.local_addr
        port = session.local_port
        created = session.created

        client = QStandardItem(client)
        client.setEditable(False)

        addr = QStandardItem(addr)
        addr.setEditable(False)

        port = QStandardItem(str(port))
        port.setEditable(False)

        created = QStandardItem(str(created.replace(microsecond=0)))
        created.setEditable(False)

        connections_model.appendRow([
            client, addr, port, created
        ])
    return connections_model


def get_client_stats_model():
    clients = get_clients()

    stats_model = QStandardItemModel()
    stats_model.setHorizontalHeaderLabels([
        'Client', 'Last login', 'Sent messages', 'Gotten messages'
    ])

    for client in clients:
        client_name = client.name
        last_login = client.sessions.order_by(ClientSession.created.desc()).first().created
        sent_messages_qty = client.sent_messages.count()
        gotten_messages_qty = client.gotten_messages.count()

        client_name = QStandardItem(client_name)
        client_name.setEditable(False)

        last_login = QStandardItem(str(last_login.replace(microsecond=0)))
        last_login.setEditable(False)

        sent_messages_qty = QStandardItem(str(sent_messages_qty))
        sent_messages_qty.setEditable(False)

        gotten_messages_qty = QStandardItem(str(gotten_messages_qty))
        gotten_messages_qty.setEditable(False)

        stats_model.appendRow([
            client_name, last_login, sent_messages_qty, gotten_messages_qty
        ])
    return stats_model
