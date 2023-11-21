import requests
import time
import os
from dotenv import load_dotenv


def get_hh_vacancies():
    url = "https://api.hh.ru/vacancies"
    lang_vacancies = {}
    programming_languages = ["Python", "JavaScript", "Java",
                             "Ruby", "C++", "PHP"]
    for language in programming_languages:
        vacancy_name = "Программист {0}".format(language)
        current_page = 0
        pages_number = 1
        vacancies_found = 0
        vacancies_salary = []
        while current_page < pages_number:
            params = {
                "text": vacancy_name,
                "area": 1,
                "only_with_salary": True,
                "page": current_page
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            time.sleep(1)  # для избегания превышения количества запросов к Api
            pages_number = response.json()["pages"]
            current_page += 1
            print(current_page, pages_number)
            for vacancy in response.json()["items"]:
                rub_salary = predict_rub_salary_hh(vacancy)
                if rub_salary:
                    vacancies_salary.append(rub_salary)
        vacancies_found += response.json()["found"]
        lang_vacancies.update(
            {
                language: {
                    "vacancies_found": vacancies_found,
                    "vacancies_processed": len(vacancies_salary),
                    "average_salary": int(sum(vacancies_salary)
                                          / len(vacancies_salary))
                }
            }
        )
    print(lang_vacancies)


def get_superjob_vacancies():
    load_dotenv()
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": os.environ["SUPERJOB_KEY"]
    }

    lang_vacancies = {}
    programming_languages = ["python", "JavaScript", "C#",
                             "Go", "C++", "PHP"]
    for language in programming_languages:
        current_page = 0
        more_pages = True
        vacancies_found = 0
        vacancies_salary = []
        while more_pages is True:
            params = {
                "catalogues": 48,
                "town": 4,
                "keyword": language,
                "count": 100,
                "page": current_page
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            more_pages = response.json()["more"]
            for vacancy in response.json()["objects"]:
                rub_salary = predict_rub_salary_sj(vacancy)
                if rub_salary:
                    vacancies_salary.append(rub_salary)
        vacancies_found += response.json()["total"]
        lang_vacancies.update(
            {
                language: {
                    "vacancies_found": vacancies_found,
                    "vacancies_processed": len(vacancies_salary),
                    "average_salary": int(sum(vacancies_salary)
                                          / len(vacancies_salary))
                }
            }
        )
    print(lang_vacancies)


def predict_rub_salary(salary_from, salary_to):
    rub_salary = 0
    if salary_from:
        if salary_to:
            rub_salary = (salary_from + salary_to) / 2
        else:
            rub_salary = salary_from * 1.2
    else:
        rub_salary = salary_to * 0.8
    return int(rub_salary)


def predict_rub_salary_hh(vacancy):
    if vacancy["salary"].get("currency") != "RUR":
        return None
    else:
        return predict_rub_salary(
            vacancy["salary"].get("from"),
            vacancy["salary"].get("to")
        )


def predict_rub_salary_sj(vacancy):
    if vacancy.get("currency") != "rub":
        return None
    else:
        return predict_rub_salary(
            vacancy.get("payment_from"),
            vacancy.get("payment_to")
        )


def main():
    get_hh_vacancies()
    get_superjob_vacancies()


if __name__ == "__main__":
    main()
