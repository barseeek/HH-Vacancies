# Programming Vacancies Comparison

The project is designed to compare job vacancies for programmers in Moscow from two popular job search platforms - [HeadHunter](https://hh.ru/) and [Superjob](https://superjob.ru/).

## Installation

1. Clone the repository to your computer:
    ```
    git clone https://github.com/barseeek/Vacancies.git
    ```
2. Navigate to the project directory:
    ```
    cd Vacancies
    ```
3. Install the necessary dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Create a `.env` file in the project's root directory and add the required environment variable - [SUPERJOB_KEY](https://api.superjob.ru/register):
    ```
    SUPERJOB_KEY=your_superjob_api_key
    ```
2. Run the script to compare vacancies:
    ```
    python vacancies.py
    ```

## Project Goals

This code is created for educational purposes as part of an online course for web developers at dvmn.org.
