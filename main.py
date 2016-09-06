from message_sender import MessageSender

if __name__ == '__main__':
    ms = MessageSender('config.ini')
    ms.test_message()
    # ms.send_messages()
