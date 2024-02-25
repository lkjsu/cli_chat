# cli_chat

To clone the Repository:
```
git clone https://github.com/lkjsu/cli_chat.git
```
Enter the cliChat directory
To run server in a separate container
```
docker build -t chat-server .
docker run -p 3874:3874 chat-server
```
Open up two clients to see messages sent and received.
To quit
```
> q
```
in the client CLI.
