from pydantic import BaseModel, Field
from scrapegraphai.graphs import SmartScraperGraph
from mpira.settings import ollama_config


def get_data(
    prompt: str,
    url: str,
    response_model=None,
    config=ollama_config,
):
    scraper = SmartScraperGraph(
        prompt=prompt,
        source=url,
        config=config,
        schema=response_model,
    )
    _ = response_model

    response = scraper.run()

    return response


class Company(BaseModel):
    name: str = Field(description="Company's name")
    description: str = Field(description="The description of the company")
    email: str = Field(description="Company's email")


def main():
    prompt = "Find some information about what does the company do, the name and a contact email."
    url = "https://scrapegraphai.com/"

    results = get_data(prompt=prompt, url=url, response_model=Company)
    print(results)


if __name__ == "__main__":
    main()
