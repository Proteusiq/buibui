from mpira.buibui import get_data, Company


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
    results = get_data(prompt=prompt, url=url, response_model=Company)

    # Assert
    assert results == expected
