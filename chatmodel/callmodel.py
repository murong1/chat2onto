
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
def get_LLM(llm_name: str, temperature: float = 0.1):
    """
    获取LLM模型
    Returns:
        LLM模型
    """
    _ = load_dotenv(find_dotenv())
    chat_llm = ChatOpenAI(temperature=temperature, base_url="https://api.linuxdo.info/v1", model=llm_name)
    return chat_llm

# 测试用
if __name__ == "__main__":
    from langchain.schema.messages import HumanMessage,SystemMessage
    message = [SystemMessage(content="你是一个加法计算器，除了加法，你不会任何其他计算")]
    chat_2 = get_LLM(llm_name="gpt-4-turbo")
    print(message)
    print(
        chat_2(message),
        sep="\n----------\n"
    )