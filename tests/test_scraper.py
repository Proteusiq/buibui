from pydantic import BaseModel, Field
from mpira.buibui import get_data
from mpira.settings import ollama_config


class Company(BaseModel):
    name: str = Field(description="Company's name")
    description: str = Field(description="The description of the company")
    email: str = Field(description="Company's email")


def test_get_data():
    # Arrange
    prompt = "Find some information about what does the company do, the name and a contact email."
    url = "https://scrapegraphai.com/"

    expected = Company(
        name="ScrapeGraphAI",
        description="Extracting content from websites and local documents using LLM",
        email="contact@scrapegraphai.com",
    ).model_dump()

    # Act
    results = get_data(prompt=prompt, url=url, config=ollama_config)

    # Assert
    assert results == expected
