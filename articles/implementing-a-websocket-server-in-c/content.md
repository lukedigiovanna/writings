The WebSocket standard is useful for persistent two-way communication in web-based environments. This is what enables real time applications in browsers such as chat applications and multiplayer games.

WebSockets are an upgraded HTTP connection that is built on TCP. 

For more information on the standard, refer to the [RFC 6455](https://datatracker.ietf.org/doc/rfc6455/?include_text=1).

This article will walk through the development of the simplest implementation of a WebSocket server in C using only Linux system calls (no libraries!)

## TCP

To be able to establish a WebSocket connection, we need to be able to handle HTTP requests, which is just a protocol built on top of TCP. So really the first thing we need to do is set up a server to receive TCP connections.

### Connecting a server

We open a socket to receive connections with the `socket(2)` system call as follows. (Note that I omitted error checking after syscalls here to make the important functionality clear, but it is good practice to always check for return errors when making syscalls).

```c
// Set up a socket server
int server_socket_fd;
struct sockaddr_in server_address;

// Create socket file descriptor
server_socket_fd = socket(AF_INET, SOCK_STREAM, 0);

server_address.sin_family = AF_INET;
server_address.sin_port = htons(PORT);
server_address.sin_addr.s_addr = htonl(INADDR_ANY);

// Bind the socket file descriptor to the address
bind(server_socket_fd, &server_address, sizeof(struct sockaddr_in));
```

### Receiving clients

After configuring the server socket, we tell it to 

## Resources Used

[Mozilla's HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

[Mozila's Writing WebSocket servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers)

