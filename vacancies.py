import requests


def predict_rub_salary(vacancy):
    rub_salary = 0
    salary_from = vacancy["salary"].get("from")
    salary_to = vacancy["salary"].get("to")
    if vacancy["salary"].get("currency") != "RUR":
        return None
    if salary_from:
        if salary_to:
            rub_salary = (salary_from + salary_to) / 2
        else:
            rub_salary = salary_from * 1.2
    else:
        rub_salary = salary_to * 0.8
    return int(rub_salary)


def main():
    url = "https://api.hh.ru/vacancies"
    lang_vacancies = {}
    programming_languages = ["Python", "JavaScript", "Java",
                             "Ruby", "PHP", "C++"]
    for language in programming_languages:
        vacancy_name = "Программист {0}".format(language)
        params = {
            "text": vacancy_name,
            "area": 1,
            "only_with_salary": True
        }
        response = requests.get(url, params=params)
        vacancies_salary = []
        for vacancy in response.json()["items"]:
            rub_salary = predict_rub_salary(vacancy)
            if rub_salary:
                vacancies_salary.append(rub_salary)
        lang_vacancies.update(
            {
                language: {
                    "vacancies_found": response.json()["found"],
                    "vacancies_processed": len(vacancies_salary),
                    "average_salary": int(sum(vacancies_salary)
                                          / len(vacancies_salary))
                }
            }
        )        
    print(lang_vacancies)


if __name__ == "__main__":
    main()
