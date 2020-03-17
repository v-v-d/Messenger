from PyQt5.QtGui import QStandardItemModel, QStandardItem

from db.utils import get_connections, get_client_stats


def get_connections_table():
    connections_table = QStandardItemModel()
    connections_table.setHorizontalHeaderLabels([
        'Client id', 'Client', 'IP address', 'Port', 'Created'
    ])

    connections = get_connections()

    if connections:
        for connection in connections:
            client_id = str(connection.client.id)
            client = connection.client.name
            addr = connection.addr
            port = str(connection.port)
            created = str(connection.created.replace(microsecond=0))

            row_list = get_row_list(client_id, client, addr, port, created)
            connections_table.appendRow(row_list)

    return connections_table


def get_client_stats_table():
    stats = QStandardItemModel()
    stats.setHorizontalHeaderLabels([
        'Client id', 'Client', 'Last login', 'Sent messages', 'Gotten messages'
    ])

    client_stats = get_client_stats()

    if client_stats:
        for stat in client_stats:
            client_id = stat.client_id
            client_name = stat.client_name
            last_login = stat.last_login
            sent_messages_qty = stat.sent_messages_qty
            gotten_messages_qty = stat.gotten_messages_qty

            row_list = get_row_list(client_id, client_name, last_login, sent_messages_qty, gotten_messages_qty)
            stats.appendRow(row_list)

    return stats


def get_row_list(*row_names):
    return [create_new_row(row_name) for row_name in row_names]


def create_new_row(row_name):
    row = QStandardItem(row_name)
    row.setEditable(False)
    return row
