# pip install python-telegram-bot
import json
import subprocess
import telegram.ext

with open('token.txt', 'r') as f:
    TOKEN = f.read()

log_filename = "log.log"
hosts_list_filename = "hosts_list.json"
template_host_list_filename = "template_host_list.json"


class PingManager:


    def __init__(self, host):
        self.host = host
        t = threading.Thread(target=self.ping)
        t.start()


    def ping(self):
        time.sleep(2)
        print("2 second")
        return (subprocess.getoutput(f"ping -w 3 {self.host}"))


def start(update, context):
    print("Function | start\n")

    update.message.reply_text("""
    Hello, this is a ping tester bot
    Please select add a new host using the following command:

    /add_host <host address>

    Or start the ping using the following command:

    /start_ping
    """)
    chat_id = update.message["chat"]["id"]
    print("Start function")
    print(f'This is the chat_id {chat_id}')


def add_host(update, context):
    print("Function | add_host\n")

    update.message.reply_text("New host is being added")

    # Get the exact part of the message that says the host address
    new_host = update.message['text'].split()
    print(f"New host added: {new_host[1]}")

    # Read the setup file
    with open(hosts_list_filename, "r") as f:
        file = json.load(f)

    file['hosts'].append(new_host[1])

    # Write the changes in the setup file
    with open(hosts_list_filename, "w") as f:
        f.write(json.dumps(file, indent=4))

    update.message.reply_text("New host has been added")

def list_hosts(update, context):
    print("Function | list_hosts\n")

    with open(hosts_list_filename, "r") as f:
        file = json.load(f)
    # Send default host to telegram
    update.message.reply_text(f"The default host is {file['default_host']}")

    # Send hosts list to telegram
    hosts_list_string = "Hosts List:\n"
    for host in file['hosts']:
        hosts_list_string += host + "\n"
    update.message.reply_text(hosts_list_string)


def set_default_host(update, context):
    print("Function | set_default_host\n")

    update.message.reply_text("The default host is being set")

    # Get the exact part of the message that says the host address
    default_host = update.message['text'].split()

    # Read the setup file
    with open(hosts_list_filename, "r") as f:
        file = json.load(f)

    # If default host is a string
    if "." in default_host[1]:
        file['default_host'] = default_host[1]
    # If default host is a index of the hosts list
    else:
        file['default_host'] = file['hosts'][int(default_host[1]) - 1]

    print(f"Set default host to: {file['default_host']}")
    # Write the changes in the setup file
    with open(hosts_list_filename, "w") as f:
        f.write(json.dumps(file, indent=4))

    update.message.reply_text(f"The default host is now {file['default_host']}")

def clear_host(update, context):
    print("Function | clear_host\n")

    update.message.reply_text("The hosts are being cleared")

    # Read the template setup file and rewrite the setup file
    with open(template_host_list_filename, "r") as template_f:
        template_file = json.load(template_f)
        with open(hosts_list_filename, "w") as f:
            f.write(json.dumps(template_file, indent=4))

    # Feedback via telegram
    update.message.reply_text("The hosts list is clear")

def start_ping(update, context):
    print("Function | start_ping\n")

    update.message.reply_text("Starting Ping")

    command = update.message['text'].split()

    # Read the setup file
    with open(hosts_list_filename, "r") as f:
        hosts_list = json.load(f)

    print(command)
    # If no argument was send
    if len(command) == 1:
        ping_response = ping(hosts_list['default_host'])
    # If some argument was send
    elif len(command) == 2:
        # Selects if the full address was send of if the index of a host in the
        # hosts list was send
        if "." in command[1]:
            ping_response = ping(command[1])
        else:
            ping_response = ping(hosts_list['hosts'][int(command[1]) - 1])
    # If an invalid argument was send
    else:
        update.message.reply_text("An invalid argument was send")
        ping_response = 0

    if ping_response != 0:
        update.message.reply_text(f"{ping_response}")
        parse_ping_response(ping_response, log_filename)


def help(update, context):
    print("Function | help\n")

    update.message.reply_text("""
    With this bot you can use the following commands:

    /start
    /add_host [address]
    /list_hosts
    /set_default_host [address|host_index]
    /clear_host
    /start_ping [address|host_index]
    /help
    /contact
    """)


def contact(update, context):
    print(f"Function | contact\n")

    update.message.reply_text("""
    Hey, great seeing you here!
    If you want to talk to the develop or send some feedback
    about the app, just send a email:

    jschmidtcordeiro@gmail.com

    And if you want to see more projects like this
    look at the Github:

    J-Cordeiro
    """)

def start_multiple_ping(update, context):
    print(f"Function | start_multiple_ping")

    command = update.message['text'].split()
    print(PingManager(command[1]).ping())
    print(PingManager(command[2]).ping())

def start_constant_ping(update, context):
    print(f"Function | start_constant_ping")
    # TODO
    # Function that allows the user to ping constantly to a certain place
    # and when stops pinging the telegram bot reports it
    # Use threads to make this function


def ping(host):
    print("Function | ping\n")

    # Here goes the ping function
    response = subprocess.getoutput(f"ping -w 3 {host}")
    print(f"Response type is: {type(response)}")
    print(f"Response is: {response}")
    return response


def parse_ping_response(ping_response, log_filename: str):
    print("Function | parse_ping_response\n")

    # Split first line
    treated_ping_response = ping_response.split("\n", 1)
    # Split blank line
    treated_ping_response = treated_ping_response[1].split("\n\n", 1)
    print(treated_ping_response)

    print(treated_ping_response[0])


def main():
    print("Function | main\n")

    updater = telegram.ext.Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start", start))
    disp.add_handler(telegram.ext.CommandHandler("add_host", add_host))
    disp.add_handler(telegram.ext.CommandHandler("list_hosts", list_hosts))
    disp.add_handler(telegram.ext.CommandHandler("set_default_host", set_default_host))
    disp.add_handler(telegram.ext.CommandHandler("clear_host", clear_host))
    disp.add_handler(telegram.ext.CommandHandler("start_ping", start_ping))
    disp.add_handler(telegram.ext.CommandHandler("help", help))
    disp.add_handler(telegram.ext.CommandHandler("contact", contact))
    # disp.add_handler(telegram.ext.CommandHandler("start_constant_ping", start_constant_ping))
    disp.add_handler(telegram.ext.CommandHandler("start_multiple_ping", start_multiple_ping))

    updater.start_polling()
    updater.idle()

    # Start the ping thread
    # x = threading.Thread(target=ping, args=(host,))
    # print("Start thread")
    # x.start()
    # x.join()
    # print("Finish thread")


if __name__ == "__main__":
    main()
