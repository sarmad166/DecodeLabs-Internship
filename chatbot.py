import random
import re
import json
import os
import time
import difflib
from datetime import datetime



BOT_NAME = "CodeBuddy"
PROFILE_FILE = "codebuddy_profile.json"   
LOG_FILE = "codebuddy_chat_log.txt"       
HISTORY_LIMIT = 10                        
TYPING_EFFECT = True                      
FUZZY_CUTOFF = 0.82                       



responses = {

    "greeting": [
        "Hey! 😄 How are you?",
        "Hello! 🤖 What's going on?",
        "Hi! Nice to see you 😄",
        "Hey there! Batao kya scene hai?",
        "Hello! Kese ho?"
    ],

    "how_are_you": [
        "I'm doing great! 😄 Tum sunao?",
        "I'm good! Thanks for asking 😊 Tumhara kya haal hai?",
        "Main theek hoon yar 😄 tum batao?",
        "All good here! 🤖 How about you?"
    ],

    "positive": [
        "That's great to hear! 😄",
        "Nice! Keep it up 🔥",
        "Wah! That's good 😊",
        "Great yar! 😄"
    ],

    "negative": [
        "Ohh 😕 kya hua?",
        "Aww, I hope things get better soon.",
        "Kya scene hai yar? Sab theek hai?",
        "Sounds rough 😕 agar baat karna chaho to batao."
    ],

    "tired": [
        "Phir thora rest kar lo yar 😅",
        "You should take a little break. Fresh mind se kaam better hota hai 😊",
        "Haan yar, rest zaroori hai. Thora relax karo 😄",
        "Long day lag raha hai 😅 thora break le lo."
    ],

    "thanks": [
        "You're welcome! 😊",
        "Koi baat nahi yar! 😄",
        "Anytime! 🤖",
        "No problem!",
        "Khushi hui help karke 😄"
    ],

    "sorry": [
        "It's okay! 😊",
        "No worries yar.",
        "Koi baat nahi 😄",
        "Don't worry about it!"
    ],

    "goodbye": [
        "Goodbye! 👋 Take care.",
        "Allah Hafiz! 👋 Phir baat hoti hai.",
        "See you later! 😄",
        "Bye! Have a great day 🤖"
    ],

    "laugh": [
        "😂😂 Haha!",
        "Hahaha 😄",
        "Yar tum bhi 😂",
        "😂 That's funny!"
    ],

    "compliment": [
        "Haha thanks! 😄",
        "Aww, thank you! 🤖❤️",
        "You're too kind 😄",
        "Thanks yar! I appreciate it."
    ],

    "identity": [
        "I'm CodeBuddy 🤖, your rule-based Python chatbot.",
        "Mera naam CodeBuddy hai 🤖.",
        "I'm CodeBuddy! I can chat with you and answer different types of questions."
    ],

    "capabilities": [
        "I can have casual conversations, remember your name, track mood, "
        "answer technical questions, and understand English + Roman Urdu.",
        "Main casual baat-cheet, naam yaad rakhna, mood track karna, "
        "technical questions aur English/Roman Urdu handle kar sakta hoon 😄.",
        "I can talk about programming, AI, Python, databases, and also "
        "normal everyday conversations. Type 'help' to see everything!"
    ],

    "unknown": [
        "Hmm 🤔 I didn't completely understand that.",
        "Acha 😄 thora aur explain karo.",
        "Interesting! Tell me a little more.",
        "Mujhe poori tarah samajh nahi aya 😅 thora detail mein batao.",
        "Hmm, let's talk about it. Thora aur batao?"
    ]
}




technical_responses = {

    "python": [
        "Python is a high-level programming language known for its simple and readable syntax.",
        "Python ek popular programming language hai jo software development, automation, data science aur AI mein use hoti hai.",
        "Python beginners ke liye bhi easy language hai aur iski bohat sari libraries available hain."
    ],

    "programming": [
        "Programming means writing instructions that tell a computer what to do.",
        "Programming ka matlab computer ko instructions dena hota hai taake wo specific task perform kare.",
        "Coding is basically the process of creating instructions for a computer."
    ],

    "ai": [
        "AI stands for Artificial Intelligence. It focuses on making computers perform tasks that normally require human-like intelligence.",
        "AI ka matlab Artificial Intelligence hai. Is mein machines ko intelligent tasks perform karne ke liye design kiya jata hai.",
        "AI is a broad field that includes areas like Machine Learning, Computer Vision and Natural Language Processing."
    ],

    "machine_learning": [
        "Machine Learning is a branch of AI where computers learn patterns from data.",
        "Machine Learning mein computer data se patterns learn karta hai aur un patterns ki base par predictions ya decisions karta hai.",
        "ML is commonly used for prediction, classification, recommendation systems and many other tasks."
    ],

    "database": [
        "A database is a system used to store, organize and manage data.",
        "Database mein data ko organized form mein store aur manage kiya jata hai.",
        "SQL is commonly used to interact with relational databases."
    ],

    "html": [
        "HTML is used to structure the content of web pages.",
        "HTML web page ka basic structure banane ke liye use hoti hai.",
        "HTML gives structure to a webpage, while CSS is mainly used for styling."
    ],

    "css": [
        "CSS is used to style and design web pages.",
        "CSS website ki styling ke liye use hoti hai, jaise colors, fonts, spacing aur layout.",
        "HTML structure banata hai aur CSS us structure ko visually style karta hai."
    ],

    "sql": [
        "SQL is used to work with relational databases.",
        "SQL databases mein data insert, retrieve, update aur delete karne ke liye use hoti hai.",
        "Common SQL operations include SELECT, INSERT, UPDATE and DELETE."
    ],

   

    "loops": [
        "Loops are used to repeat a block of code multiple times, like 'for' and 'while' loops.",
        "Loops se ek hi code ko baar baar chalaya jata hai, jaise for loop aur while loop.",
        "A 'for' loop is great when you know how many times to repeat; 'while' is better when it depends on a condition."
    ],

    "functions": [
        "A function is a reusable block of code that performs a specific task.",
        "Function ek reusable code block hota hai jo ek specific kaam perform karta hai.",
        "Functions help you avoid repeating the same code again and again."
    ],

    "oop": [
        "OOP (Object-Oriented Programming) organizes code using classes and objects.",
        "OOP mein code ko classes aur objects ki soorat mein organize kiya jata hai.",
        "The four main pillars of OOP are Encapsulation, Abstraction, Inheritance and Polymorphism."
    ],

    "data_structure": [
        "A data structure is a way of organizing and storing data so it can be used efficiently.",
        "Data structure data ko organize aur store karne ka tarika hai taake use efficiently access kiya ja sake.",
        "Common data structures include arrays, linked lists, stacks, queues, trees and graphs."
    ],

    "git": [
        "Git is a version control system used to track changes in code.",
        "Git ek version control system hai jo code ki changes track karta hai.",
        "GitHub is a platform where Git repositories can be hosted and shared online."
    ],

    "exception_handling": [
        "Exception handling lets you deal with errors gracefully using try, except, and finally.",
        "Exception handling se errors ko gracefully handle kiya jata hai, try aur except ki madad se.",
        "Without exception handling, one error can crash your entire program."
    ]
}




keyword_groups = {

    "python": ["python", "py", "python language"],
    "programming": ["programming", "programmer", "coding", "code", "coding language"],
    "ai": ["artificial intelligence", "ai"],
    "machine_learning": ["machine learning", "machine-learning", "ml"],
    "database": ["database", "databases", "db", "mysql", "dbms"],
    "html": ["html"],
    "css": ["css"],
    "sql": ["sql"],
    "loops": ["loop", "loops", "for loop", "while loop"],
    "functions": ["function", "functions", "def"],
    "oop": ["oop", "object oriented", "class", "classes", "inheritance"],
    "data_structure": ["data structure", "data structures", "array", "linked list", "stack", "queue", "tree", "graph"],
    "git": ["git", "github", "version control"],
    "exception_handling": ["exception", "exception handling", "try except", "error handling"]
}


_flat_keyword_to_topic = {}
for _topic, _keywords in keyword_groups.items():
    for _kw in _keywords:
        _flat_keyword_to_topic[_kw] = _topic




def load_profile():
    """Agar pehle se profile file maujood hai to usay load karo."""
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_profile(profile):
    """Naam wagera ko JSON file mein save kar do (agli dafa ke liye)."""
    try:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    except OSError:
        pass 




def log_conversation(user_text, bot_text):
    """Har turn ko timestamp ke sath log file mein append karo."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] You: {user_text}\n")
            f.write(f"[{timestamp}] Bot: {bot_text}\n\n")
    except OSError:
        pass




def clean_input(text):
    """Input ko lowercase, extra spaces aur punctuation se saaf karo."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)         
    text = re.sub(r"[!?.,;:]+", "", text)     
    return text



def fuzzy_topic_match(text):
    """
    Agar koi word technical keyword se milta julta ho (typo ke sath),
    to bhi sahi topic dhoond lo. Sirf 4+ letters wale words check
    karte hain taake chotay words galat match na karein.
    """
    words = text.split()
    all_keywords = list(_flat_keyword_to_topic.keys())

    for word in words:
        if len(word) < 4:
            continue

        matches = difflib.get_close_matches(
            word, all_keywords, n=1, cutoff=FUZZY_CUTOFF
        )

        if matches:
            return _flat_keyword_to_topic[matches[0]]

    return None




def detect_language(text):
    roman_urdu_words = [
        "kya", "kia", "hai", "hy", "ho", "hun", "mujhe", "mera", "meri",
        "mere", "tum", "aap", "ap", "kaise", "kese", "acha", "achha",
        "yar", "yaar", "mujh", "batao", "btao", "chahiye", "nahi", "nai",
        "kyun", "kyo", "kab", "abhi", "aj", "aaj", "kal", "bohat", "bahut",
        "shukriya", "maaf", "karna", "seekhna", "seekhni", "kar", "kr",
        "tha", "thi"
    ]

    words = text.split()
    urdu_count = sum(1 for word in words if word in roman_urdu_words)

    if urdu_count >= 2:
        return "roman_urdu"
    return "english"




def time_greeting():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning! ☀️"
    elif 12 <= hour < 17:
        return "Good afternoon! 🌤️"
    elif 17 <= hour < 21:
        return "Good evening! 🌆"
    else:
        return "Working late? 🌙"




def matches_any(text, phrases):
    """
    'hi' in 'history' == True hota hai simple substring check se -
    ye bug purane code mein bhi tha. Isliye ab \\b (word boundary)
    use karte hain taake sirf poora word/phrase match ho, andar
    chupa hua substring nahi.
    """
    for phrase in phrases:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        if re.search(pattern, text):
            return True
    return False


def detect_intent(text, context):

   
    goodbye_words = ["bye", "goodbye", "see you", "see ya", "exit",
                      "quit", "allah hafiz", "khuda hafiz"]
    if matches_any(text, goodbye_words):
        return "goodbye"

    
    help_words = ["help", "menu", "commands", "options",
                  "madad", "kya kya options hain"]
    if matches_any(text, help_words):
        return "help"

    
    reset_words = ["reset", "reset karo", "clear chat", "start over",
                   "naya session"]
    if matches_any(text, reset_words):
        return "reset"

    
    mood_words = ["mood report", "mera mood", "how is my mood",
                  "mood kaisa hai", "mood kesa hai"]
    if matches_any(text, mood_words):
        return "mood_report"


    greetings = ["hello", "hi", "hey", "salam", "assalam o alaikum",
                 "assalamualaikum", "aoa", "good morning", "good evening",
                 "good afternoon", "kya haal", "kia haal", "kese ho",
                 "kaise ho", "kesy ho"]
    if matches_any(text, greetings):
        return "greeting"

    how_are_you = ["how are you", "how r u", "how are u", "how you doing",
                   "how is it going", "kya haal hai", "kia haal hai",
                   "kese ho", "kaise ho", "sab theek", "sab thik"]
    if matches_any(text, how_are_you):
        return "how_are_you"

    name_patterns = ["my name is ", "mera naam ", "mera nam ", "my name's "]
    for pattern in name_patterns:
        if text.startswith(pattern):
            name = text.replace(pattern, "").strip()
            if name:
                context["name"] = name.title()
                return "name"

    ask_name = ["what is my name", "whats my name", "do you know my name",
                "mera naam kya hai", "mera nam kya hai",
                "tumhe mera naam pata hai", "apko mera naam pata hai"]
    if matches_any(text, ask_name):
        return "ask_name"

    identity = ["who are you", "what are you", "your name", "tum kon ho",
                "tum kaun ho", "ap kon ho", "aap ka naam kya hai",
                "tumhara naam kya hai"]
    if matches_any(text, identity):
        return "identity"

    capabilities = ["what can you do", "what do you do", "your capabilities",
                    "how can you help", "mujhe kis cheez mein help",
                    "tum kya kar sakte ho", "aap kya kar sakte ho"]
    if matches_any(text, capabilities):
        return "capabilities"

    thanks = ["thanks", "thank you", "thank u", "thx", "shukriya",
              "bohat shukriya", "thanks yar"]
    if matches_any(text, thanks):
        return "thanks"

    sorry = ["sorry", "i am sorry", "my bad", "maaf karna", "sorry yar"]
    if matches_any(text, sorry):
        return "sorry"

    positive_words = ["good", "great", "fine", "awesome", "excellent",
                       "happy", "nice", "amazing", "theek", "acha",
                       "achha", "khush", "mast", "zabardast"]
    if any(word in text.split() for word in positive_words):
        return "positive"

    negative_words = ["sad", "upset", "angry", "bad", "depressed",
                       "worried", "tension", "stress", "pareshan",
                       "udaas", "dukhi", "gussa"]
    if any(word in text.split() for word in negative_words):
        return "negative"

    tired_words = ["tired", "exhausted", "so tired", "bohat thak",
                   "bahut thak", "thak gaya", "thak gya", "thak gayi",
                   "thak gyi"]
    if matches_any(text, tired_words):
        return "tired"

    laugh_words = ["haha", "hahaha", "lol", "lmao", "hehe"]
    if matches_any(text, laugh_words) or "😂" in text:
        return "laugh"

    compliment_words = ["you are smart", "you are good", "you are amazing",
                        "good bot", "nice bot", "smart bot", "tum smart ho",
                        "aap smart ho", "acha bot"]
    if matches_any(text, compliment_words):
        return "compliment"

    technical_priority = ["machine_learning", "database", "sql", "python",
                          "html", "css", "ai", "programming", "loops",
                          "functions", "oop", "data_structure", "git",
                          "exception_handling"]

    for topic in technical_priority:
        if matches_any(text, keyword_groups[topic]):
            return topic

    fuzzy_topic = fuzzy_topic_match(text)
    if fuzzy_topic:
        return fuzzy_topic

   
    follow_up_words = ["tell me more", "explain more", "more about it",
                       "what about it", "why", "how does it work",
                       "explain it", "aur batao", "mazeed batao",
                       "thora aur batao", "ye kaise kaam karta hai",
                       "ye kya hai", "is ke bare mein batao",
                       "iske bare mein batao"]
    if matches_any(text, follow_up_words):
        if context.get("last_topic"):
            return "follow_up"

    memory_questions = ["what did i say", "what did i tell you",
                        "do you remember", "remember my last message",
                        "meri last baat kya thi", "maine kya kaha tha",
                        "ma ne kya kaha tha", "tumhe yaad hai"]
    if matches_any(text, memory_questions):
        return "memory"


    history_words = ["show history", "chat history", "conversation history",
                     "our conversation", "history dikhao",
                     "hamari conversation", "hamari chat"]
    if matches_any(text, history_words):
        return "history"

    return "unknown"




def get_technical_response(topic):
    if topic in technical_responses:
        return random.choice(technical_responses[topic])
    return None


def get_follow_up_response(context):
    topic = context.get("last_topic")

    follow_up_texts = {
        "python": "Python ke bare mein aur baat karein 😄 Python mein "
                  "variables, lists, functions, OOP aur libraries jaise "
                  "NumPy aur Pandas important concepts hain.",
        "programming": "Programming ko practice se best samjha ja sakta "
                       "hai. Pehle basic logic, conditions, loops aur "
                       "functions strong karo.",
        "ai": "AI ek broad field hai. Is mein Machine Learning, Deep "
              "Learning, NLP aur Computer Vision jaise areas shamil hain.",
        "machine_learning": "Machine Learning mein usually data collect "
                            "kiya jata hai, phir model ko train karke "
                            "predictions ya classifications ki jati hain.",
        "database": "Database mein data organized form mein store hota "
                    "hai. Relational databases mein tables aur SQL "
                    "commonly use hote hain.",
        "html": "HTML webpage ka structure banati hai. Iske common "
                "elements headings, paragraphs, links, images aur forms "
                "hain.",
        "css": "CSS webpage ko style karti hai. Is se colors, fonts, "
               "spacing, borders aur layouts control kiye ja sakte hain.",
        "sql": "SQL mein SELECT, INSERT, UPDATE aur DELETE basic "
               "operations hain. Inhein CRUD operations se bhi relate "
               "kiya jata hai.",
        "loops": "Loops mein 'for' loop tab use hota hai jab pata ho "
                 "kitni baar repeat karna hai, aur 'while' loop tab jab "
                 "condition par depend karta ho.",
        "functions": "Functions ko 'def' keyword se banaya jata hai. "
                     "Ye code ko organized aur reusable banate hain.",
        "oop": "OOP ke 4 pillars hain: Encapsulation, Abstraction, "
               "Inheritance aur Polymorphism. Ye large projects ko "
               "manage karna asaan banate hain.",
        "data_structure": "Data structures data ko efficiently store "
                          "karne ka tarika batate hain - jaise stack "
                          "LIFO follow karta hai aur queue FIFO.",
        "git": "Git commits ke zariye code ki history track karta hai, "
              "aur branches se tum alag features par kaam kar sakte ho.",
        "exception_handling": "try block mein risky code likha jata hai, "
                              "aur except block mein us se hone wali "
                              "error ko handle kiya jata hai."
    }

    return follow_up_texts.get(topic, random.choice(responses["unknown"]))


def get_help_response():
    return (
        "\n📋 CodeBuddy Pro - Kya kya kar sakta hoon:\n"
        "  • Casual chat (greetings, mood, jokes)\n"
        "  • Naam yaad rakhna ('my name is ...')\n"
        "  • Technical Q&A: python, sql, database, ai, oop, git, "
        "loops, functions, data structures\n"
        "  • 'mood report'   -> ab tak ka mood summary\n"
        "  • 'chat history'  -> pichli conversation dikhana\n"
        "  • 'reset'         -> sab kuch clear karna\n"
        "  • 'bye'           -> chatbot band karna\n"
    )


def get_mood_report(context):
    score = context.get("mood_score", 0)

    if score > 2:
        return f"Tumhara overall mood positive raha hai is session mein 😄 (score: {score})"
    elif score < -2:
        return f"Lagta hai session thora tough raha 😕 (score: {score}). Sab theek hai?"
    else:
        return f"Tumhara mood is session mein balanced raha hai 🙂 (score: {score})"


def get_response(intent, context):

    if intent in responses:
        return random.choice(responses[intent])

    if intent == "name":
        name = context.get("name")
        return f"Nice to meet you, {name}! 😄"

    if intent == "ask_name":
        if context.get("name"):
            return f"Your name is {context['name']} 😄"
        return "Abhi mujhe tumhara naam nahi pata. Batao, tumhara naam kya hai?"

    if intent == "help":
        return get_help_response()

    if intent == "reset":
        context["name"] = None
        context["last_topic"] = None
        context["mood_score"] = 0
        context["history"] = []
        return "Sab kuch reset ho gaya 🔄 Chalo naye se shuru karte hain!"

    if intent == "mood_report":
        return get_mood_report(context)

    technical_response = get_technical_response(intent)
    if technical_response:
        return technical_response

    if intent == "follow_up":
        return get_follow_up_response(context)

    if intent == "memory":
        history = context["history"]
        if not history:
            return "Abhi hamari koi previous conversation nahi hai."
        last_message = history[-1]["user"]
        return f"Tumne last kaha tha: \"{last_message}\""

    if intent == "history":
        history = context["history"]
        if not history:
            return "Abhi conversation history empty hai."

        result = "\n"
        for chat in history:
            result += f"You: {chat['user']}\n"
            result += f"Bot: {chat['bot']}\n"
        return result

    return random.choice(responses["unknown"])




TECHNICAL_TOPICS = [
    "python", "programming", "ai", "machine_learning", "database",
    "html", "css", "sql", "loops", "functions", "oop",
    "data_structure", "git", "exception_handling"
]


def print_bot_message(message):
    """Optional typing effect - taake bot thora natural lage."""
    if TYPING_EFFECT:
        print("Bot: ", end="", flush=True)
        for ch in message:
            print(ch, end="", flush=True)
            time.sleep(0.01)
        print()
    else:
        print("Bot:", message)


def main():

    profile = load_profile()

    context = {
        "name": profile.get("name"),
        "last_topic": None,
        "last_message": "",
        "mood_score": 0,
        "history": []
    }

    print("=" * 60)
    print(f"🤖 {BOT_NAME} Pro")
    print("Rule-Based | English + Roman Urdu | No AI / No API")
    print(time_greeting())
    if context["name"]:
        print(f"Welcome back, {context['name']}! 😄")
    print("Type 'help' for options, 'bye' to exit.")
    print("=" * 60)

    while True:

        user_input = input("\nYou: ")
        cleaned = clean_input(user_input)

        if not cleaned:
            print("Bot: Kuch type bhi karo 😄")
            continue

        context["last_message"] = cleaned
        language = detect_language(cleaned)
        intent = detect_intent(cleaned, context)

        if intent == "goodbye":
            response = get_response(intent, context)
            print_bot_message(response)
            log_conversation(user_input, response)

            if context.get("name"):
                save_profile({"name": context["name"]})

            break

        response = get_response(intent, context)
        print_bot_message(response)


        if intent == "positive":
            context["mood_score"] += 1
        elif intent == "negative":
            context["mood_score"] -= 1

      
        if intent in TECHNICAL_TOPICS:
            context["last_topic"] = intent

        context["history"].append({
            "user": user_input,
            "bot": response,
            "intent": intent,
            "language": language
        })

        if len(context["history"]) > HISTORY_LIMIT:
            context["history"].pop(0)

        log_conversation(user_input, response)

      
        if intent == "name" and context.get("name"):
            save_profile({"name": context["name"]})


if __name__ == "__main__":
    main()