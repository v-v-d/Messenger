Messenger
=======

GUI application for secure sending messages between multiple users and storing message history on server.

Set it up
------

1 Clone github repository with server and client code and go to the root directory

    $ git clone https://github.com/v-v-d/Messenger.git
    $ cd Messenger
    
2 Get python venv module if it's not exists

    $ sudo apt-get install python3-venv
    
3 Create a virtual environment, update pip and install the requirements

    $ python3 -m venv ./venv
    $ source ./venv/bin/activate
    $ pip3 install --upgrade pip
    $ pip3 install -r requirements.txt
    
4 Set up database config and ip-address with port for the server
    
    $ nano ./server/config.yaml

5 Run the server GUI (-m key for creating database)

    $ python server -m

6 Run the client GUI (ip-address and port must be the same as in step 4)

    $ python client -a <server ip-address> -p <server port>
