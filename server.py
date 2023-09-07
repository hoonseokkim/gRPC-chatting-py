from concurrent import futures
from collections import deque

import asyncio

import grpc
import chatting_pb2
import chatting_pb2_grpc
import pytest

import time

class Chatting(chatting_pb2_grpc.ChattingServicer):
    def __init__(self, event_loop) -> None:

        print("Server started.")
        self.channel_list = {}  # dict channel_name : [users]
        self.messages = deque()
        
        # 10초마다 알림
        event_loop.create_task(self.__alarm_timer(interval=10))

    async def __alarm_timer(self, interval: float):
        while True:
            request = chatting_pb2.ChatRequest()
            request.cmd = "alarm"
            request.message = time.strftime('%M:%S')
            print(request)
            self.messages.append(request)
            await asyncio.sleep(interval)

    async def MakeChannel(self, request, context):
        channel_name = request.channel_name
        success_or_not = chatting_pb2.SuccessOrNot()

        if request.channel_name in self.channel_list.keys():
            success_or_not.success = False

        else:
            self.channel_list[channel_name] = [request.user_name]

            success_or_not.success = True

        print(f"Made the channel {channel_name}")

        print(self.channel_list)
        return success_or_not

    async def ShowChannelPeople(self, request, context):
        return_channel_people = chatting_pb2.ChannelPeople()

        return_channel_people.people_list[:] = self.channel_list[request.channel_name]
        
        print("show channel people.")
        return return_channel_people

    async def ShowChannel(self, request, context):
        return_channel_list = chatting_pb2.ChannelList()
        return_channel_list.channel_list[:] = list(self.channel_list.keys())

        print('show channel.')

        print(self.channel_list)
        return return_channel_list

    async def EnterChannel(self, request, context):
        if request.channel_name in self.channel_list.keys():

            self.channel_list[request.channel_name].append(request.user_name)
            success_or_not = chatting_pb2.SuccessOrNot()
            success_or_not.success = True
            print(self.channel_list)

            return success_or_not

        else:
            success_or_not = chatting_pb2.SuccessOrNot()
            success_or_not.success = False

            print(self.channel_list)

            return success_or_not

    async def ExitChannel(self, request, context):
        self.channel_list[request.channel_name].remove(request.user_name)

        if not self.channel_list[request.channel_name]:
            del self.channel_list[request.channel_name]

        success_or_not = chatting_pb2.SuccessOrNot()
        success_or_not.success = True

        print(self.channel_list)

        return success_or_not

    def ChatStream(self, request_iterator, context):
        last_index = 0
        while True:
            while len(self.messages) > last_index:
                message = self.messages[last_index]
                if message.cmd != "alarm":
                    print('stream chat')
                last_index += 1
                yield message

    async def SendChat(self, request, context):
        user_name = request.user_name
        message = request.message
        channel_name = request.channel_name

        print(f'[{channel_name}] {user_name} : {message}')

        self.messages.append(request)
        print('chat received.')
        return chatting_pb2.Empty()


async def serve(event_loop):

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    chatting_pb2_grpc.add_ChattingServicer_to_server(Chatting(event_loop), server)

    server.add_insecure_port('[::]:11912')
    await server.start()


    try:
        await server.wait_for_termination()

    except KeyboardInterrupt:
        await server.stop(0)

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(serve(loop))
    
    except KeyboardInterrupt:
        print("Server closed.")
        loop.close()
        quit()