# Chat Application using Brainfuck

![Ewor Asci Art - Client.bf](visuals/ewor_art.PNG)

## Demo

![chat](visuals/chat.gif)

## How to run

Run **one instance of the server** and **two instances of the client**.

```bash
python brainfuck.py server.bf
python brainfuck.py client.bf
```

You can also run ```asci_art_client.bf``` for the client, depending on your **aestetic preferences :D**.

## How it works

![brainfuck_diagram](visuals/Diagram.PNG)

The main program is **client.bf**. It waits for input from a queue (```,``` returns the first element of the queue and Null if the queue is empty). The queue is filled by the users input (getch.py) or from the server. It then recognizes the origin of the message and outputs it whenever an "enter" is reached. So it waits for you to complete the message before sending it to the server.

If you typed the message, it gets a **"You:"** prefix, if it is from the other person it gets a **"Other:"** prefix.

The **server.bf** is a simple echo server. It waits for input from the client and then sends it back to the other client as input.

The networking is implemented using sockets in python. It forwards the output from the clients to the input of the server and vice versa.

The interpreter for the brainfuck code is also written in python (brainfuck.py).


## Brainfuck Code Features

- **Anker Trick**: Setting a cell to 255 to be able to come back to it from anywhere (```+[-<+]-```). 
- **While Loop**: Multiple while loops are used to wait for user input and the enter key.
- **If-statements**: If-statements are for example used to check if the user has pressed the enter key.
- **If-else-statements**: If-else-statements are for example used to check if the message is from the own client or the other client and print the prefix accordingly.
- **Inverting 0**: convert 0 to something nonzero and nonzero numbers to zero (this is negation in Brainfuck; very useful for if-statements).
