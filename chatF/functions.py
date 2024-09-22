from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
import chatmodel.callmodel as callmodel
from vector_stores import getBackgroundText


def user_story_generator(message, history):
    instructions = [SystemMessage(content="You are a conversational ontology engineering assistant."),
                    HumanMessage(
                        content="I am a domain expert trying to create a user story to be used by ontology engineers."
                                " You are the ontology expert. Only ask the following question once I have responded. Ask for the"
                                "specifications to generate a user story as a user of the system, which should include: 1. The "
                                "Persona: What are the name, occupation, skills and interests of the user? 2. The Goal: What is "
                                "the goal of the user? Are they facing specific issues? 3. Example Data: Do you have examples of "
                                "the specific data available? Make sure you have answers to all three questions before providing "
                                "a user story. The user story should be written in the following structure: title, persona, goal, "
                                "scenario (where the user could use a structured knowledge base to help with their work), and "
                                "example data. Only ask the next question once I have responded. And you should also ask questions "
                                "to elaborate on more information after the user provides the initial information, and ask for "
                                "feedback and suggestions after the user story is generated.")]

    messages = build_messages(history)
    messages.append({
        "role": "user",
        "content": message
    })
    chat_LLM = callmodel.get_LLM(llm_name="gpt-3.5-turbo")
    response = chat_LLM.invoke(instructions + messages)
    parser = StrOutputParser()
    bot_message = parser.invoke(response)
    history.append([message, bot_message])
    return bot_message, history, ""


def cq_generator(message, history):
    """
    generate competency questions based on the user story
    format constraint may not be necessary if we only use LLMs for clustering
    :param message:
    :param history:
    :return:
    """
    instructions = [{
        "role": "system",
        "content": "You are a conversational ontology engineering assistant."
    }, {
        "role": "user",
        "content": "Here are instructions for you on how to generate high-quality competency questions. First, here "
                   "are some good examples of competency questions generated from example data. Who performs the song? "
                   "from the data Yesterday was performed by Armando Rocca, When (what year) was the building built? "
                   "from the data The Church was built in 1619, In which context is the building located? from the "
                   "data The Church is located in a periurban context. Second, how to make them less complex. Take the "
                   "generated competency questions and check if any of them can be divided into multiple questions. If "
                   "they do, split the competency question into multiple competency questions. If it does not, leave "
                   "the competency question as it is. For example, the competency question Who wrote The Hobbit and in "
                   "what year was the book written? must be split into two competency questions: Who wrote the book? "
                   "and In what year was the book written?. Another example is the competency question, When was the "
                   "person born?. This competency question cannot be divided into multiple questions. Third, how to "
                   "remove real entities to abstract them. Take the competency questions and check if they contain "
                   "real-world entities, like Freddy Mercury or 1837. If they do, change those real-world entities "
                   "from these competency questions to more general concepts. For example, the competency question "
                   "Which is the author of Harry Potter? should be changed to Which is the author of the book?. "
                   "Similarly, the competency question Who wrote the book in 2018? should be changed to Who wrote the "
                   "book, and in what year was the book written?"
    }]
    messages = build_messages(history)
    messages.append({
        "role": "user",
        "content": message
    })
    chat_LLM = callmodel.get_LLM(llm_name="gpt-3.5-turbo")
    response = chat_LLM.invoke(instructions + messages)
    parser = StrOutputParser()
    bot_message = parser.invoke(response)
    history.append([message, bot_message])
    return bot_message, history, ""


def build_messages(history):
    """
    convert gardio.Chatbot history to OpenAI client messages
    :param history:
    :return:
    """
    messages = list()
    for item in history:
        messages.append({"role": "user", "content": item[0]})
        messages.append({"role": "system", "content": item[1]})
    return messages[1:]


def genKG_generator():
    backText = getBackgroundText('TCP guarantees the reliable, in-order delivery of a stream of bytes')


