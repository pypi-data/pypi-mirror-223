from opaw import util
from opaw.examples import setup
from opaw.model.chat import ChatBot

def loop_chat(model="gpt-3.5-turbo",
              system_prompt="You are a helpful assistant.",
              history_file="history"):
    bot = ChatBot(model)
    bot.add_message(system_prompt, role="system")
    print("(type \"bye\" to quit.)")
    while True:
        user_input = input("User: ")
        if "bye" in user_input:
            print("BYE!")
            break
        response = bot.create(user_input)
        bot_response = response["choices"][0]["message"]["content"]
        print(f"Bot: {bot_response}\n")

    util.save_history(bot, history_file)


# api key
setup()

# start model
loop_chat()

# You can also set system prompt if needed
# util.loop_chat(system_prompt="You are a liar. So you always have to lie to me.")
