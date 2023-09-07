
# Requirement

1. install
```
$ pip install -r requirements.txt
```

2. compile proto file
```
$ python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. chatting.proto
```


# How to run

1. open terminal and run this for server.
```
$ python server.py
```

2. open another terminal and run this for user's CLI env
```
$ python chatting_cli.py
```

# Guide for user

1. first, you have to put user name.
```
Welcome to MyPrivateChatting!
Please Write your name.
Name : //put your name.
```

2. If so, You could see main menu. You can choose from that what todo in here, like Entering or available to see channels that others made, making channel. 

Also, regardless of channels, you can speak to users which joined to chatting service.

```
        Main Session
            # 1 : Enter channel
            # 2 : Show channel list
            # 3 : Make channel
            # Also you can speak to all of people by using !all     
            # example) !all hello
```

3. If you enter the certain channel, you could see sub menu. You can choose from that what todo in here, too. If there is no one in channel, channel deleted. In here, you can interact with people who joined the same channel. also, in need you can speak to all of users by using !all. 

If there is no one in channel, channel will be deleted. 
```
        Sub Session
            # 1 : Exit Channel
            # 2 : Enter another channel
            # 3 : Show users in this channel
            # Also you can speak to all of people by using !all     
            # example) !all hello
```
