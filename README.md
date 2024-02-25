# cli_chat

Clone the repo
```
git clone https://github.com/lkjsu/cli_chat.git
```
#### To run dockerized server
```
docker build -t chat-server .
docker run -p 3874:3874 chat-server
```
Once the server is up spin up two clients to see messages sent and received.
To quit
```
> q
```
in the client CLI
