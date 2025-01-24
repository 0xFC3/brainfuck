import threading
import queue
import sys

class _Getch:
    """Gets a single character from standard input."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class BufferedGetch:
    def __init__(self):
        self._getch = _Getch()
        self.input_queue = queue.Queue()
        self._running = True
        self._input_thread = threading.Thread(target=self._input_worker, daemon=True)
        self._input_thread.start()
        self.on_keyboard_input = None 
        
    def _input_worker(self):
        while self._running:
            try:
                char = self._getch()
                # Echo the character
                if isinstance(char, bytes):
                    decoded = char.decode('ascii')
                else:
                    decoded = char
                if ord(decoded) == 13:  # Enter key
                    sys.stdout.write('\n')
                else:
                    sys.stdout.write(decoded)
                sys.stdout.flush()
                self.input_queue.put((char, True))
            except:
                pass
                
    def add_input(self, text):
        for char in text:
            self.input_queue.put((char, False))
        
    def __call__(self):
        return self.getch()
        
    def getch(self):
        try:
            char, is_keyboard = self.input_queue.get_nowait()
            if is_keyboard and self.on_keyboard_input:
                self.on_keyboard_input()  
            return char
        except queue.Empty:
            return chr(0)  
            
    def __del__(self):
        self._running = False
        if hasattr(self, '_input_thread'):
            self._input_thread.join(timeout=0.1)


# Create a single instance to be used by the interpreter
_getch_instance = BufferedGetch()
getch = _getch_instance.getch
add_input = _getch_instance.add_input
input_queue = _getch_instance.input_queue
set_keyboard_callback = lambda cb: setattr(_getch_instance, 'on_keyboard_input', cb)

