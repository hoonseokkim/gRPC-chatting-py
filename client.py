import grpc
import threading

import chatting_pb2
import chatting_pb2_grpc
import time
address = 'localhost'
port = 11912


class Client:

    def __init__(self, user_name) -> None:
        self.user_name = user_name
        self.channel = ''

        channel = grpc.insecure_channel(address+':'+str(port))
        self.conn = chatting_pb2_grpc.ChattingStub(channel)

        # self.conn.TimeStream(request, timeout=5)
        threading.Thread(target=self.listen_messages, daemon=True).start()

    def make_channel_request(self, channel_name: str):
        channel_make_req = chatting_pb2.GiveUserAndChannel()

        channel_make_req.user_name = self.user_name
        channel_make_req.channel_name = channel_name

        success = self.conn.MakeChannel(channel_make_req).success

        if success:
            self.channel = channel_name

        return success

    def enter_channel_request(self, channel_name):
        enter_channel_req = chatting_pb2.GiveUserAndChannel()

        enter_channel_req.user_name = self.user_name
        enter_channel_req.channel_name = channel_name

        success = self.conn.EnterChannel(enter_channel_req).success

        if success:
            self.channel = channel_name

        return success

    def exit_channel_request(self):
        exit_channel_req = chatting_pb2.GiveUserAndChannel()

        exit_channel_req.user_name = self.user_name
        exit_channel_req.channel_name = self.channel

        success = self.conn.ExitChannel(exit_channel_req).success

        if success:
            self.channel = ''

        return success

    def get_channel_list(self):
        show_channel = self.conn.ShowChannel(chatting_pb2.Empty())

        if show_channel.channel_list:
            channel_list = show_channel.channel_list

            return channel_list

    def get_user_list(self):
        user_list_req = chatting_pb2.ShowPeopleRequest()
        user_list_req.channel_name = self.channel

        user_list = self.conn.ShowChannelPeople(user_list_req).people_list

        return user_list

    def __handle_msg_cmd(self, msg):
        if msg.cmd == "alarm" and msg.message == time.strftime('%M:%S'):
            print(f"[알림] {msg.message} 입니다.")

    def listen_messages(self):
        try:
            for msg in self.conn.ChatStream(chatting_pb2.Empty()):
                if msg.cmd:
                    self.__handle_msg_cmd(msg)

                elif self.channel == msg.channel_name:
                    print(f"[{msg.channel_name}] {msg.user_name} : {msg.message}")

                elif msg.channel_name == "all":
                    print(f"[{msg.channel_name}] {msg.user_name} : {msg.message}")
        
        except:
            print("Server closed.")
            quit()

    def send_message(self, message, all=False):
        # message 형식 -> [channel_name] user_name : msg (스트림할 때..)
        chat_req = chatting_pb2.ChatRequest()

        chat_req.user_name = self.user_name

        if all:
            chat_req.channel_name = "all"
        else:
            chat_req.channel_name = self.channel

        chat_req.message = message

        self.conn.SendChat(chat_req)
