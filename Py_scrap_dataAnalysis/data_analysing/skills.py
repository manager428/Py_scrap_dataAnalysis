import csv


def extract_skills_from_descriptions():
    skills = [
        "Python",
        "GIT",
        "SQL",
        "REST",
        "API",
        "Docker",
        "AWS",
        "Linux",
        "Django",
        "Postgresql",
        "Artificial Intelligence",
        "JS",
        "Machine Learning",
        "react",
        "OOP",
        "Flask",
        "NoSQL",
        "Networking",
        "Fullstack",
        "microservice",
        "MongoDB",
        "HTML",
        "CSS",
        "algorithms",
        "DRF",
        "FastAPI",
        "asyncio",
        "GraphQL",
    ]

    skills_count = {}

    with open(
        "../data/python_vacancies.csv", "r", newline="", encoding="utf-8"
    ) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            description = row[1].lower()

            for skill in skills:
                if skill.lower() in description:
                    skills_count[skill] = skills_count.get(skill, 0) + 1



    with open(
            "../data/skills.csv", "w", newline="", encoding="utf-8"
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Skill", "Total"])

        for skill, count in skills_count.items():
            writer.writerow([skill, count])


if __name__ == "__main__":
    extract_skills_from_descriptions()
