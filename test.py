from disinter.disinter import ApplicationCommandOptionChoice


a = ApplicationCommandOptionChoice(name="sample", value=123)

print(a.to_json())
