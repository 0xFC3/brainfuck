import sys, getch, socket, threading
from time import sleep

# Globals
cells = [0] * 30000
is_client = False
sock = None
other_sock = None

def evaluate(code):
    global cells
    code = cleanup(list(code))
    bracemap = buildbracemap(code)
    codeptr = cellptr = 0

    while codeptr < len(code):
        cmd = code[codeptr]
        
        if cmd == ">": cellptr = (cellptr + 1) % 30000
        elif cmd == "<": cellptr = (cellptr - 1) % 30000
        elif cmd == "+": cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        elif cmd == "-": cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        elif cmd == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
        elif cmd == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
        elif cmd == ".":
            char = chr(cells[cellptr])
            sys.stdout.write('\n' if cells[cellptr] == 13 else char)
            sys.stdout.flush()
            if is_client and cells[29998]: send(char)
        elif cmd == ",":
            char = getch.getch()
            cells[cellptr] = ord(char.decode('ascii') if isinstance(char, bytes) else char)
            
        codeptr += 1

def cleanup(code): return ''.join(c for c in code if c in '.,[]<>+-')

def execute(filename):
    # Set keyboard input callback
    def on_keyboard():
        global cells
        cells[29998] = 1
    getch.set_keyboard_callback(on_keyboard)
    
    # Start networking if needed
    if filename.endswith('server.bf'): start_server()
    elif filename.endswith('client.bf'): connect_client()
    
    # Run program
    evaluate(open(filename).read())
    
    # Keep server running if we're the server
    if filename.endswith('server.bf'):
        try:
            while True: sleep(1)
        except KeyboardInterrupt: pass
    
    # Cleanup
    if sock: sock.close()
    if other_sock: other_sock.close()

def buildbracemap(code):
    stack, bmap = [], {}
    for pos, cmd in enumerate(code):
        if cmd == "[": stack.append(pos)
        elif cmd == "]":
            start = stack.pop()
            bmap[start] = pos
            bmap[pos] = start
    return bmap

def relay(src, dst=None):
    while True:
        try:
            data = src.recv(1024)
            if not data: break
            if dst: dst.send(data)
            else: getch.add_input(data.decode())
        except: break
    src.close()

def handle_server():
    global sock, other_sock
    sock = socket.socket()
    sock.bind(('localhost', 5000))
    sock.listen(2)
    c1, _ = sock.accept()
    c2, _ = sock.accept()
    threading.Thread(target=relay, args=(c1, c2), daemon=True).start()
    threading.Thread(target=relay, args=(c2, c1), daemon=True).start()

def start_server():
    # Start server in background thread
    threading.Thread(target=handle_server, daemon=True).start()

def connect_client():
    global sock, is_client
    sock = socket.socket()
    sock.connect(('localhost', 5000))
    is_client = True
    threading.Thread(target=relay, args=(sock,), daemon=True).start()

def send(char):
    if is_client and sock:
        try: sock.send(char.encode())
        except: pass

def main():
    if len(sys.argv) == 2: execute(sys.argv[1])
    else: print("Usage:", sys.argv[0], "filename")

if __name__ == "__main__": main()

