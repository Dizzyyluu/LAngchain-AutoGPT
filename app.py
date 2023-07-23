
import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import prompts
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
#install the following libraries 
#Streamlit used to build the app
#LAngchain - used to build the llm workflow
#openAI 0- needed to use OPENAI GPT
#Wikipedia - used to connect GPT to wikipedia
#CHROMADB - vector storage 
#TIKTOKEN - Backend tokenizer for openai

os.environ['OPENAI_API_KEY'] = apikey

st.title('AutoGPT')
prompt = st.text_input('Enter your prompt here')

title_template = PromptTemplate(
    input_variable = ['topic']
    template = 'write me a youtube video title about {topic}'
)

script_template = PromptTemplate(
    input_variable = ['title', 'wikipedia_research'],
    template = 'write me a youtube script based on this title Title: {title} while leveraging this wikipedia research:{wikipedia_research}'
)


#Memory
title_memory = ConversationBufferMemory(input_key = 'topic', memory_key= 'chat_history')
script_memory = ConversationBufferMemory(input_key = 'title', memory_key= 'chat_history')


#LLMS
llm = OpenAI(temperature = 0.9)
title_chain = LLMChain(llm = llm, prompt = title_template, verbose = True, output_key = 'title', memory = title_memory)
script_chain = LLMChain(llm = llm, prompt = script_template, verbose = True, output_key = 'script', memory = script_memory)
sequential_chain = SimpleSequentialChain(chains= [title_chain, script_chain,], input_variables = ['topic'],
                                         output_variables =['title', 'script'], verbose = True)

wiki = WikipediaAPIWrapper()

#trigger our prompt to the LLM

#Display output on the screen
if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain.run(title = title, wikipedia_research = wiki_research)

    st.write(response['title'])
    st.write(response['script'])

    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)

    with st.expander('Wikipedia History'):
        st.info(wiki_research)

    