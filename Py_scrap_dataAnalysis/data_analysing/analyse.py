import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ALL_DATA = "../data/python_vacancies.csv"
TECHNOLOGIES = "../data/skills.csv"


def preprocess_salary(salary):
    if pd.notnull(salary):
        salary = salary.strip().replace("$", "").replace(",", "").strip()
        if "-" in salary:
            salary = max(int(value[-4:]) for value in salary.split("-"))
        elif salary.startswith("до") or salary.startswith("від"):
            salary = int(salary[-4:])
    else:
        salary = 0
    return salary


def analyze_skills():
    skills_data = pd.read_csv(TECHNOLOGIES, usecols=["Skill", "Total"])
    skills_data.plot.bar(x="Skill", y="Total", rot=90, legend=False, alpha=0.5)
    plt.xlabel("Skills")
    plt.ylabel("Total")
    plt.title("Skills Analysis")
    plt.tight_layout()
    plt.show()


def analyze_applicants():
    applicants_data = pd.read_csv(ALL_DATA, usecols=["title", "applications"])
    top_applicants = applicants_data.nlargest(50, "applications").sort_values(
        "applications", ascending=True
    )
    top_applicants.plot.barh(x="title", y="applications", figsize=(10, 12))
    plt.xlabel("Applicants")
    plt.ylabel("Job Offers")
    plt.title("Applicants for Top 50 Job Offers")
    plt.tight_layout()
    plt.show()


def analyze_job_offers_by_experience(vacancies_file):
    df_vacancies = pd.read_csv(vacancies_file)
    offers_by_experience = df_vacancies["experience"].value_counts().sort_index()
    offers_by_experience.plot(kind="bar")
    plt.xlabel("Years of Experience")
    plt.ylabel("Number of Job Offers")
    plt.title("Job Offers by Years of Experience")
    plt.tight_layout()
    plt.show()


def perform_correlation_analysis(vacancies_file, skills_file, top_n=50):
    df_vacancies = pd.read_csv(vacancies_file)
    df_skills = pd.read_csv(skills_file)
    df_vacancies["salary"] = df_vacancies["salary"].apply(preprocess_salary)
    columns = ["experience", "salary", "views", "applications"]

    skill_correlations = {}
    for skill in df_skills["Skill"]:
        skill_vacancies = df_vacancies[
            df_vacancies["description"].str.contains(skill, case=False, na=False)
        ]
        correlation_matrix = skill_vacancies[columns].corr()
        skill_correlations[skill] = correlation_matrix

    top_skills = sorted(
        skill_correlations,
        key=lambda x: np.mean(np.abs(skill_correlations[x])),
        reverse=True,
    )[:top_n]
    combined_matrix = np.array(
        [skill_correlations[skill].mean().values for skill in top_skills]
    )

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        combined_matrix,
        annot=True,
        xticklabels=columns,
        yticklabels=top_skills,
        cmap="coolwarm",
    )
    plt.title(f"Correlation Matrix for Top {top_n} Skills")
    plt.xlabel("Parameters")
    plt.ylabel("Skills")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analyze_skills()
    analyze_applicants()
    perform_correlation_analysis(ALL_DATA, TECHNOLOGIES)
    analyze_job_offers_by_experience(ALL_DATA)
