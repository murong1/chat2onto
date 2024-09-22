import gradio as gr

from chatF.functions import *

from vector_stores import getBackgroudText

getBackgroudText = getBackgroudText.getBackgroudText()
with gr.Blocks() as user_story_interface:
    # 仅仅是一个markdown
    gr.Markdown(
        """
        #新建demo
        用于生成需求文档的背景功能
        """
    )
    with gr.Row():
        with gr.Column():
            # 起始的一句话
            user_story_chatbot = gr.Chatbot([
                [None, "Hello! I am OntoChat, your conversational ontology engineering assistant. I will guide you step"
                       " by step in the creation of a user story. Let's start with the persona. What are the name, "
                       "occupations, skills, interests of the user?"],
            ])
            #输入框
            user_story_input = gr.Textbox(
                label="Chatbot input",
                placeholder="Please type your message here and press Enter to interact with the chatbot :)"
            )

        # 生成的user story
        user_story = gr.TextArea(
            label="User story",
            interactive=True
        )
    user_story_input.submit(
        fn=user_story_generator,
        inputs=[
            user_story_input, user_story_chatbot
        ],
        outputs=[
            user_story, user_story_chatbot, user_story_input
        ]
    )

with gr.Blocks() as cq_interface:
    gr.Markdown(
        """
        # demo
        生成CQ
        """
    )
    with gr.Row():
        with gr.Column():
            cq_chatbot = gr.Chatbot([
                [None, "I am OntoChat, your conversational ontology engineering assistant. Here is the second step of "
                       "the system. Please give me your user story and tell me how many competency questions you want "
                       "me to generate from the user story."]
            ])
            cq_input = gr.Textbox(
                label="Chatbot input",
                placeholder="Please type your message here and press Enter to interact with the chatbot :)"
            )
        cq_output = gr.TextArea(
            label="Competency questions",
            interactive=True
        )
    cq_input.submit(
        fn=cq_generator,
        inputs=[
            cq_input, cq_chatbot
        ],
        outputs=[
            cq_output, cq_chatbot, cq_input
        ]
    )

with gr.Blocks() as genKG_interface:
    gr.Markdown(
        """
        # demo
        生成KG
        """
    )
    with gr.Row():
        with gr.Column():
            genKG_input = gr.Textbox(
                label="CQ input",
                placeholder="Please type your message here and press Enter to interact with the chatbot :)"
            )
        genKG_output = gr.TextArea(
            label="Knowledge graphs",
            interactive=True
        )
        with gr.Column():
            files = gr.File(label="Upload Knowledge Base",
                            file_types=['.txt', '.md', '.docx', '.pdf', '.pptx', '.epub', '.xlsx'])
            with gr.Row():
                upload = gr.Button("Upload")

    genKG_input.submit(
        fn=genKG_generator,
        inputs=[
            genKG_input,
        ],
        outputs=[
            genKG_output, genKG_input
        ]
    )
    def upload_kb(file_paths):
        gr.Info("Uploading KnowledgeBase...")
        getBackgroudText.upload_kb(file_paths)
        gr.Info("Upload Successfully!")

demo = gr.TabbedInterface(
    [user_story_interface, cq_interface, genKG_interface],
    ["User Story Generation", "Competency Question Extraction","genKG"]
)
if __name__ == "__main__":
    demo.launch()
