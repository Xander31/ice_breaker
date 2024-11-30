import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from third_party.linkedin import scrape_linkedin_profile
from third_party.x import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.x_lookup_agent import lookup_x_username as x_lookup_agent


def ice_breaker_with(name:str):
    linkedin_url_profile = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url_profile, mock=True)

    x_username = x_lookup_agent(name)
    x_posts = scrape_user_tweets(username=x_username, num_tweets= 3, mock= True)

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    summary_template = """
        Given the information about a person from LinkedIn: {information}, and latest X (Twitter) posts {x_posts}.
        Using BOTH information from LinkedIn and X (Twitter), I want you to create:
        1) A short summary. (Max 3 sentences).
        2) Give 2 interesting facts about the person and his/her posts.
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "x_posts"],
        template=summary_template
    )

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data, "x_posts": x_posts})

    print(res)

if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")

    ice_breaker_with(name="Donald Trump")


