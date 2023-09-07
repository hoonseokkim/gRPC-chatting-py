from re import L
from client import Client
import sys, select

class ChattingCLI:

    def __init__(self, client):
        self.client = client
        self.main_menu = {'1', '2', '3'}

    @staticmethod
    def welcome():
        user_name = input("""
        Welcome to MyPrivateChatting!
        Please Write your name.
        Name : """)

        while not user_name:
            print("Write your user name properly.")
            user_name = input("Name : ")

        return user_name

    def show_make_channel(self, channel_name):
        success = self.client.make_channel_request(channel_name)

        if success:
            print(f"\n\n# Entered to channel {self.client.channel}\n")

            self.show_channel_menu()

        else:
            print("The channel name alread have.")
            self.show_main_menu()

    def show_enter_channel(self):
        channel_name = input("# Which channel you want to go?")

        success = self.client.enter_channel_request(channel_name)

        if success:
            print(f"# You entered to the channel [{channel_name}]\n")
            self.show_channel_menu()

        else:
            print(f"# channel [{channel_name}] does not exist.\n")
            self.show_main_menu()

# 채널에서 대기실로 exit
# 채널에서 채널로 exit enter

    def show_exit_channel(self, go_another=False):
        out_channel = self.client.channel

        success = self.client.exit_channel_request()

        if success:
            print(f"\n# You exited channel [{out_channel}].\n")

            if not go_another:
                self.show_main_menu()
            else:
                self.show_enter_channel()

        else:
            print("Something has wrong. Try it again.\n")

    def show_user_list(self):
        print("===========USER LIST==========")

        user_list = self.client.get_user_list()

        for user in user_list:
            print(f"●{user}")

    def show_channel_list(self):
        print("\n===========Channel_list==========")
        channel_list = self.client.get_channel_list()

        if channel_list:
            for channel in channel_list:
                print(f'# Channel name : {channel}')

        else:
            print("# There is no channel.\n")
    def __print_info_message(self, is_main: bool = False, is_sub: bool = False):
        if is_main:
            print("""
        <<<<<Main Session>>>>>
            # 1 : Enter channel
            # 2 : Show channel list
            # 3 : Make channel
            # Also you can speak to all of peple by using !all
            # example) !all hello \n""")
        elif is_sub:
            print("""
        <<<<<Sub Session>>>>>
            # 1 : Exit Channel
            # 2 : Enter another channel
            # 3 : Show users in this channel
            # Also you can speak to all of peple by using !all
            # example) !all hello \n""")
    def show_main_menu(self):
        self.__print_info_message(is_main=True)

        # Enter channel

        # COMMAND가 아니라면 그냥 채팅하고 있다는 것.

        while True:
            try:
                selected_menu = input()

                if selected_menu == '1':
                    self.show_enter_channel() 
                    break

                    # Show channel list
                elif selected_menu == '2':
                    self.show_channel_list()

                    # Make channel
                elif selected_menu == '3':
                    channel_name = input("\n# New channel name : ")

                    while not channel_name:
                        print("Write channel name properly.")
                        channel_name = input("\n# New channel name : ")

                    self.show_make_channel(channel_name)
                    break

                elif selected_menu == '':
                    self.__print_info_message(is_main=True)
                    continue

                elif selected_menu.split()[0] == "!all":
                    self.client.send_message(' '.join(selected_menu.split()[1:]), all=True)

                else:
                    print(""" # You are not in channel. 
                    if you want to tell something,
                    use !all or enter channel """)

            except KeyboardInterrupt:
                self.__close_channel(is_main=True)

    def __close_channel(self, is_main: bool = False, is_sub: bool = False):
        if is_main == False and is_sub == False:
            return

        if is_sub:
            self.show_exit_channel()
        print("\n\n# Chatting closed. Good Bye.")
        quit()
    
    def show_channel_menu(self):
        self.__print_info_message(is_sub=True)

        try:
            while True:
                r, w, x = select.select([sys.stdin], [], [], 10)
                if r:
                    selected_menu = sys.stdin.readline().strip()
                else:
                    self.__close_channel(is_sub=True)

                if selected_menu == '1':
                    self.show_exit_channel(go_another=False)
                    break

                elif selected_menu == '2':
                    self.show_channel_list()
                    self.show_exit_channel(go_another=True)
                    break

                # Make channel
                elif selected_menu == '3':
                    self.show_user_list()

                elif selected_menu == '':
                    self.__print_info_message(is_sub=True)
                    continue

                elif selected_menu.split()[0] == "!all":
                    self.client.send_message(
                        ' '.join(selected_menu.split()[1:]), all=True)

                else:
                    self.client.send_message(selected_menu)
        except KeyboardInterrupt:
            self.__close_channel(is_sub=True)


def run():
    user_name = ChattingCLI.welcome()

    print(f"Enjoy your time in here. {user_name}\n\n")

    client = Client(user_name)
    client_CLI = ChattingCLI(client)

    client_CLI.show_main_menu()


if __name__ == '__main__':
    run()
