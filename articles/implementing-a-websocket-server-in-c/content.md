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

After configuring the server socket, we tell it to wait for a client, which opens
a file descriptor that we can read requests from.

```c
struct sockaddr client_address;
socklen_t len;
int client_fd = accept(server_socket_fd, &client_address, &len);
```

## HTTP

When we first get a connection from a client, we expect an HTTP request to 
establish the WebSocket handshake. This section requires an implementation of
HTTP. I wrote a very basic HTTP server that specifically handles the case of
setting up a WebSocket, but not much else (i.e. no sending files, handling
authentication, cookies, JSON, etc.). 

> An alternative to writing your own HTTP implementation is to use a reverse 
> proxy where you have another server setup to handle HTTP requests and sends 
> that client to your WebSocket server.

In any case, I will not walk through my HTTP implementation, but it simply
involves parsing an HTTP request.

### The WebSocket Handshake Request

The handshake must be done before data can be sent back and forth. The purpose of this handshake is for the server to prove to the client that it supports the WebSocket protocol. This is done with an HTTP request that usually looks something like:

```
GET / HTTP/1.1
Host: https://my-site.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGVzdF9rZXk=
Sec-WebSocket-Version: 13
```

The most important header here is `Sec-WebSocket-Key`. The client sends this
for the server to prove to the client that it supports the WebSocket protocol.
This process works as follows:

1. The server appends the GUID `"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"` to the provided `Sec-WebSocket-Key`. This GUID was chosen as the standard since it is "unlikely to be used by network endpoints that do not understand the WebSocket protocol"
2. Then hashes this string using SHA-1 (note the weak cryptographic security of SHA-1 is not a concern as this is primarily done just as part of the protocol, not to protect sensitive data)
3. Then base64 encodes this hash.

Then the server sends an HTTP response back to the client with the `101 Switching Protocols` status code and the result of the above process in the `Sec-WebSocket-Accept` header.

This response may look something like:

```
HTTP/1.1 101 Switching Protocols
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOr=
Connection: Upgrade
Upgrade: websocket
```

Upon receipt, the client knows that it can start sending and receiving WebSocket frames from this server.

## WebSocket Duplex Communication

The WebSocket protocol uses the concept of frames to send messages 

## Resources Used

[Mozilla's HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

[Mozila's Writing WebSocket servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers)

