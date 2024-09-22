import openai
import json

openai.api_key = 'sk-lsjVA12mNAObu3wD5d60DfC98eA3454bA8946b6eE7B9EbCb'  # 请替换为您的实际API密钥
openai.base_url = 'https://chatapi.zjt66.top/v1'
def generate_sub_questions(question):
    prompt = f"请将以下问题拆解为更小的子问题，并为每个子问题生成一个唯一的token：\n\n{question}\n\n请以JSON格式返回，格式如下：\n[\n  {{'token': 'token1', 'sub_question': '子问题1'}},\n  {{'token': 'token2', 'sub_question': '子问题2'}},\n  ...\n]"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response['choices'][0]['message']['content']
    sub_questions = json.loads(content)
    return sub_questions

def answer_sub_questions(sub_questions, context):
    answers = []
    for item in sub_questions:
        token = item['token']
        sub_question = item['sub_question']
        prompt = f"考虑到以下背景信息：\n{context}\n\n请回答以下子问题（Token: {token}）：\n{sub_question}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response['choices'][0]['message']['content']
        answers.append({'token': token, 'answer': answer})
    return answers

def combine_answers(answers):
    prompt = "请将以下子问题的答案整合为对原始问题的完整回答，确保逻辑清晰、语言流畅：\n\n"
    for item in answers:
        token = item['token']
        answer = item['answer']
        prompt += f"Token: {token}\n答案: {answer}\n\n"
    prompt += "请整合以上内容，生成最终答案。"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    final_answer = response['choices'][0]['message']['content']
    return final_answer

def main():
    question = input("请输入您的问题：")
    sub_questions = generate_sub_questions(question)
    answers = answer_sub_questions(sub_questions, question)
    final_answer = combine_answers(answers)
    print("答案：\n", final_answer)

if __name__ == "__main__":
    main()