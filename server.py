import nltk
import socket
from nltk.corpus import stopwords
stop = stopwords.words('english')

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT = '!D'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# seems to work only for specific case
def preprocess(text):
    text = ' '.join([word for word in text.split() if word not in stop])
    sentence = nltk.sent_tokenize(text)
    sentence = [nltk.word_tokenize(sent) for sent in sentence]
    sentence = [nltk.pos_tag(sent) for sent in sentence]
    return sentence


# better then above preprocessor but also breaks is name is only one word
def nl_preprocess(text):
    text = ' '.join([word for word in text.split() if word not in stop])
    words = nltk.word_tokenize(text)
    print(words)
    tagged = nltk.pos_tag(words)
    print(tagged)
    chunks = nltk.ne_chunk(tagged)
    print(chunks)
    name = ''
    for chunk in chunks:
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() == 'PERSON':
                name += ' '.join([c[0] for c in chunk])
                name += ' '

    return name


def greeting(text):
    return nl_preprocess(text)


def handle_client(conn, addr):
    print(f'NEW connection {addr} connected')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT:
                conn.send(f'Thank You'.encode(FORMAT))
                connected = False
            else:
                person = greeting(msg)
                conn.send(f'Hi, {person} how can I help YOU'.encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print('[LISTENING]...')
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)


print('[STARTING] server is starting...')
start()
