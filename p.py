context =  {}

user_input= input("YOU: ")

for user_input in "my name is sarmad":
    context["name"]= "sarmad"
    print("BOT: Nice to meet you!")
    

for user_input in "I live in Lahore":
    context["city"]="Lahore"
    print("BOT: Great!")
    

    if user_input == "what is my name":
        print("BOT: your name is ", context["name"])

    elif user_input == "where do I live":
        print("BOT: you live in ", context["city"])