from datetime import date
import json
from pathlib import Path
from pydantic import BaseModel, Field
from scrapegraphai.graphs import SmartScraperGraph
from mpira.settings import gemini_config as config


def get_data(
    prompt: str,
    url: str,
    response_model=None,
    config=config,
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


class Match(BaseModel):
    dato: date = Field(description="Game played date")
    home: str = Field(description="Name of the team playing at home")
    visitor: str = Field(description="Name of the team playing away")
    home_goals: int = Field(description="Number of goals scored by home team")
    visitor_goals: int = Field(description="Number of goals scored by away team")
    attendance: int
    url: str


class Matches(BaseModel):
    matches: list[Match] = Field(description="a list of matches")


def main():
    prompt = "Get theresults of football games"

    for start_year, end_year in ([21, 22], [22, 23], [23, 24]):
        print(f"----- Getting Data 20{start_year} - 20{end_year} ")
        url = f"https://superstats.dk/program?aar=20{start_year}%2F20{end_year}"

        results = get_data(
            prompt=prompt,
            url=url,
            response_model=Matches,
        )
        print("------ RESULTS -----")
        print(results)

        json.dump(results, Path(f"../data/{start_year}{end_year}x.json").open("w"))


if __name__ == "__main__":
    main()
