from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


def print_country(index, data):
    # skips new cases and returns the n'th total
    def get_nth_total(n, lst):
        counter = 0
        for data_point in lst:
            if '+' not in data_point or data_point != 'N/A':
                if counter == n:
                    return data_point
                else:
                    counter += 1

    def cases_str_to_int(cases):
        return int(''.join(cases.split(',')))

    def paused_print(sentence):
        print(sentence)
        time.sleep(1)

    prepend = f'{index}. ' if index else ''
    data_list = data.split(' ')
    country_name = data_list[0]

    total_cases = get_nth_total(1, data_list)
    total_cases_int = cases_str_to_int(total_cases)
    total_deaths = get_nth_total(2, data_list)
    total_deaths_int = cases_str_to_int(total_deaths)
    total_recoveries = get_nth_total(3, data_list)
    total_recoveries_int = cases_str_to_int(total_recoveries)

    mortality_rate = round(total_deaths_int/total_cases_int * 100, 1)
    recovery_rate = round(total_recoveries_int/total_cases_int * 100, 1)

    paused_print(f'{prepend}{country_name}')
    paused_print(f'Total cases: {total_cases}')
    paused_print(f'Total deaths: {total_deaths} ({mortality_rate}%)')
    paused_print(f'Total recoveries: {total_recoveries} ({recovery_rate}%)')
    paused_print('---------------------------')


def generate_formatter():
    count = 0

    def formatter(data):
        nonlocal count
        print_country(count, data)
        time.sleep(5)
        count += 1

    return formatter


if __name__ == '__main__':
    browser = webdriver.Chrome('./chromedriver')
    browser.get('https://www.worldometers.info/coronavirus/')
    while True:
        try:
            myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'nav-tabContent')))
            content = myElem.text
            countries = content.splitlines()
            countries = countries[21:39]
            format_data = generate_formatter()
            for country in countries:
                print(country)
                format_data(country)
        except TimeoutException:
            print("Loading took too much time!")
        browser.refresh()
