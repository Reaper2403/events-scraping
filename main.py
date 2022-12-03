from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from api import add_events
import json

driver = webdriver.Chrome(executable_path=r"C:\Users\KIIT\Downloads\chromedriver.exe")

# WINDOW MAXIMIZED IS NECESSARY
driver.maximize_window()


city = input('Enter location to search and enter to for india')
URL = 'https://www.eventbrite.com/d/india--' + city + '/all-events/?page=1'
driver.get(URL)


def print_events(events):
    for i in events:
        print('Heading -> ', i.get('heading'))
        print('Date ->', i.get('date'))
        print('Location ->', i.get('location'))
        print('Organiser ->', i.get('organiser'))
        print('Image ->', i.get('image'))
        print('Registration ->', i.get('registration_link'))
        print('-------------------------------------------------\n')


time.sleep(3)


def get_pages():
    pages = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/footer/div/div/ul/li[2]'
    p = driver.find_element(By.XPATH, pages).text
    return int(p.split()[-1])


def get_page_data(event_data):
    for i in range(1, 20):
        temp = {}
        try:
            heading = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[1]/section/ul/li[' + str(
                i) + ']/div/div/div[1]/div/div/div/article/div[2]/div/div/div[1]/a/h3/div/div[2]'
            date = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[1]/section/ul/li[' + str(
                i) + ']/div/div/div[1]/div/div/div/article/div[2]/div/div/div[1]/div'
            location = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[' \
                       '1]/section/ul/li[' + str(i) + ']/div/div/div[1]/div/div/div/article/div[2]/div/div/div[' \
                                                      '2]/div[1]/div '
            organiser = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[' \
                        '1]/section/ul/li[' + str(i) + ']/div/div/div[1]/div/div/div/article/div[2]/div/div/div[' \
                                                       '2]/div[3]/div/div '
            registration = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[' \
                           '1]/section/ul/li[' + str(
                i) + ']/div/div/div[2]/div/div/div/article/div[2]/aside/a'
            image = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[1]/section/ul/li[' + str(
                i) + ']/div/div/div[2]/div/div/div/article/div[2]/aside/a/div/div/img'

            heading_data = driver.find_element(By.XPATH, heading).text
            date_data = driver.find_element(By.XPATH, date).text
            location_data = driver.find_element(By.XPATH, location).text
            organiser_data = driver.find_element(By.XPATH, organiser).text
            registration_data = driver.find_element(By.XPATH, registration).get_attribute('href')
            image_data = driver.find_element(By.XPATH, image).get_attribute('src')

            temp['image'] = image_data
            event_data.append({
                'heading': heading_data,
                'date': date_data,
                'location': location_data,
                'organiser': organiser_data,
                'registration_link': registration_data
            })
        except NoSuchElementException:
            print('Element found error at ->', i)
        except:
            print('Uncaught Exception')


total_pages = get_pages()
events = []
for _ in range(total_pages - 1):
    try:
        get_page_data(events)
        next_button_path = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[' \
                           '1]/footer/div/div/ul/li[3]/button '
        next_button = driver.find_element(By.XPATH, next_button_path)
        next_button.click()
        time.sleep(3)
    except:
        break

data = json.dumps(events, indent=2)
with open('event_data.json', 'w') as f:
    f.write(data)

add_events(events)
