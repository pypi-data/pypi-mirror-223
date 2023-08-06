from opaw import util


# setup api
util.setup()

# start model
util.loop_chat()

# You can also set system prompt if need
# util.loop_chat(system_prompt="You are a liar. So you always have to lie to me.")
