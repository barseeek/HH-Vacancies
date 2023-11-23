import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_stats_vacancies_hh(area_id):
    url = "https://api.hh.ru/vacancies"
    stats_programming_vacancies = {}
    programming_languages = ["Python", "JavaScript", "C#",
                             "Go", "C++", "PHP"]
    for language in programming_languages:
        vacancy_name = "Программист {0}".format(language)
        current_page = 0
        pages_number = 1
        vacancies_found = 0
        vacancy_salaries = []
        while current_page < pages_number:
            params = {
                "text": vacancy_name,
                "area": area_id,
                "page": current_page
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            vacancies = response.json()
            pages_number = vacancies["pages"]
            current_page += 1
            for vacancy in vacancies["items"]:
                if vacancy.get("salary", None):
                    rub_salary = predict_rub_salary_hh(vacancy)
                    if rub_salary:
                        vacancy_salaries.append(rub_salary)
        vacancies_found = vacancies["found"]
        if vacancy_salaries:
            average_salary = int(sum(vacancy_salaries) / len(vacancy_salaries))
        else:
            average_salary = 0
        stats_programming_vacancies[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(vacancy_salaries),
            "average_salary": average_salary
        }
    return stats_programming_vacancies


def get_area_id_hh(country, location):
    url = "https://api.hh.ru/areas"
    response = requests.get(url)
    response.raise_for_status()
    for country in response.json():
        for area in country["areas"]:
            if area.get("name") == location:
                return area.get("id")


def get_stats_vacancies_sj(headers, town_id, catalogue_id):
    url = "https://api.superjob.ru/2.0/vacancies/"
    page_count = 100
    stats_programming_vacancies = {}
    programming_languages = ["Python", "JavaScript", "C#",
                             "Go", "C++", "PHP"]
    for language in programming_languages:
        current_page = 0
        more_pages = True
        vacancies_found = 0
        vacancy_salaries = []
        while more_pages:
            params = {
                "catalogues": catalogue_id,
                "town": town_id,
                "keyword": language,
                "count": page_count,
                "page": current_page
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            vacancies = response.json()
            more_pages = vacancies["more"]
            current_page += 1
            for vacancy in vacancies["objects"]:
                rub_salary = predict_rub_salary_sj(vacancy)
                if rub_salary:
                    vacancy_salaries.append(rub_salary)
        vacancies_found = vacancies["total"]
        if vacancy_salaries:
            average_salary = int(sum(vacancy_salaries) / len(vacancy_salaries))
        else:
            average_salary = 0
        stats_programming_vacancies[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(vacancy_salaries),
            "average_salary": average_salary
        }
    return stats_programming_vacancies


def get_town_id_sj(headers, location):
    url = "https://api.superjob.ru/2.0/towns/"
    current_page = 0
    more_pages = True
    while more_pages:
        params = {
            "page": current_page
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        towns = response.json()
        more_pages = towns["more"]
        current_page += 1
        for town in towns["objects"]:
            if town.get("title") == location:
                return town.get("id")


def get_catalogue_id_sj(headers, title):
    url = "https://api.superjob.ru/2.0/catalogues/"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    for work_area in response.json():
        if work_area.get("title") == title:
            return work_area.get("key")


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


def print_table(lang_vacancy_stats, title):
    table = [[
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата"
    ]]
    for language, vacancies_stats in lang_vacancy_stats.items():
        table.append([
            language,
            vacancies_stats.get("vacancies_found"),
            vacancies_stats.get("vacancies_processed"),
            vacancies_stats.get("average_salary"),
        ])
    print(AsciiTable(table, title).table)


def main():
    load_dotenv()
    sj_api_key = os.environ["SUPERJOB_KEY"]
    headers = {
        "X-Api-App-Id": sj_api_key
    }
    hh_area_id = get_area_id_hh("Россия", "Москва")
    sj_area_id = get_town_id_sj(headers, "Москва")
    sj_catalogue_id = get_catalogue_id_sj(
        headers,
        "Разработка, программирование"
    )
    print_table(get_stats_vacancies_hh(hh_area_id), "HeadHunter Moscow")
    print_table(
        get_stats_vacancies_sj(
            headers,
            sj_area_id,
            sj_catalogue_id
        ),
        "Superjob Moscow"
    )


if __name__ == "__main__":
    main()
