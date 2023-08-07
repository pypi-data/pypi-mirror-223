from __future__ import annotations
from langchain.vectorstores import Chroma

from typing import ClassVar, Mapping
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from langchain.llms import LlamaCpp
from langchain.memory import ConversationSummaryBufferMemory
from langchain import LLMChain, PromptTemplate
from operator import itemgetter
from langchain.chains import (
    ConversationalRetrievalChain,
    SimpleSequentialChain,
    VectorDBQA,
)
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser


# class LLM:
#     def initialize():
#         # Create the retriever
#         vectorstore = Chroma(
#             collection_name="agent-memory", persist_directory=".persitence"
#         )
#         retriever = vectorstore.as_retriever()
#         template = """Answer the question based only on the following context:
#         {context}

#         Question: {question}

#         Answer in the following language: {language}
#         """
#         prompt = ChatPromptTemplate.from_template(template)

#         chain = (
#             {
#                 "context": itemgetter("question") | retriever,
#                 "question": itemgetter("question"),
#                 "language": itemgetter("language"),
#             }
#             | prompt
#             | model
#             | StructuredOutputParser()
# )


class LLMContext(BaseModel):
    inference_chain: LLMChain

    class Config:
        arbitrary_types_allowed = True


# probably not needded
class LLMMessage(BaseModel):
    text: str
    message_id: str


@dataclass
class Plugin:
    TYPE: ClassVar[str] = "llm"
    model_name: str
    system_prompt: str = ""
    # Uses LLAMA 2 prompt format by default
    system_prompt_prefix: str = "<<SYS>>\n"
    system_prompt_postfix: str = "\n<</SYS>>\n\n"
    instruction_prefix: str = "[INST]"
    instruction_postfix: str = "[/INST]"
    model_temperature: float = 0.7
    context_size: int = 4096

    def _build_prompt_template(self) -> PromptTemplate:
        prompt_template = (
            "{instruction_prefix}"
            "{system_prompt_prefix}"
            "{system_prompt}"
            "{system_prompt_postfix}"
            "Chat History:\n\n"
            "{chat_history} \n\n"
            "Human: {user_input}"
            "{instruction_postfix}\nAI: "
        )
        prompt_template = prompt_template.format(
            instruction_prefix=self.instruction_prefix,
            system_prompt_prefix=self.system_prompt_prefix,
            system_prompt=self.system_prompt,
            system_prompt_postfix=self.system_prompt_postfix,
            instruction_postfix=self.instruction_postfix,
            chat_history="{chat_history}",
            user_input="{user_input}",
        )
        print(prompt_template)

        prompt = PromptTemplate(
            input_variables=["chat_history", "user_input"], template=prompt_template
        )
        return prompt

    def build_context(self, instance_name: str) -> Mapping:
        llm = LlamaCpp(
            model_path=self.model_name,
            n_ctx=self.context_size,
            n_gpu_layers=40,
            temperature=self.model_temperature,
        )  # type: ignore
        memory = ConversationSummaryBufferMemory(
            llm=llm,
            memory_key="chat_history",
        )
        prompt_template = self._build_prompt_template()
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            memory=memory,
            verbose=True,
        )
        llm_context = {"inference_chain": llm_chain}
        return llm_context

    def callback(self, message: Mapping, context: Mapping):
        llm_context = LLMContext(**context)
        llm_message = LLMMessage(**message)

        model = llm_context.inference_chain
        llm_message.text = model.predict(user_input=llm_message.text)

        return llm_message.dict()
