import re
from datetime import date

EXPERIENCE_START = date(2022, 3, 1)
README_PATH = "README.md"


def years_of_experience():
    today = date.today()
    years = today.year - EXPERIENCE_START.year
    if (today.month, today.day) < (EXPERIENCE_START.month, EXPERIENCE_START.day):
        years -= 1
    return years


if __name__ == "__main__":
    years = years_of_experience()

    with open(README_PATH, "r") as f:
        content = f.read()

    new_content = re.sub(
        r"<!-- YEARS_EXP -->\d+<!-- /YEARS_EXP -->",
        f"<!-- YEARS_EXP -->{years}<!-- /YEARS_EXP -->",
        content,
    )

    with open(README_PATH, "w") as f:
        f.write(new_content)

    print(f"Updated README: {years}+ years of experience.")
