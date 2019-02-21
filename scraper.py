from bs4 import BeautifulSoup
import requests
import pprint

# Task 1
def scrape_top_universities():
    url = 'https://www.timeshighereducation.com/student/best-universities/top-50-universities-reputation-2018#survey-answer'
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')

    university_table = soup.find_all('tr')
    university_table.pop(0)

    top_university_list = []
    for tr in university_table:
        university_data = tr.find_all('td')

        university_dict = {'world_rank_2018':'','world_rank_2017':'','university_name':'','country':'','world_university_rank_2018':'','university_url':''}
        university_dict['world_rank_2018'] = int(university_data[0].get_text().strip('='))
        university_dict['world_rank_2017'] = university_data[1].get_text()
        university_dict['university_name'] = university_data[2].a.get_text()
        university_dict['country'] = university_data[3].get_text()
        university_dict['world_university_rank_2018'] = university_data[4].get_text()
        university_dict['university_url'] = university_data[2].a['href']
        top_university_list.append(university_dict)

    return top_university_list
    # pprint.pprint(top_university_list)

top_universities = scrape_top_universities()
# print(top_universities)


# Task 2
def analyse_university_by_world_rank_2018(university_list):
    world_rank_2018_dict = {}
    for university in university_list:
        rank = university['world_rank_2018']
        world_rank_2018_dict[rank] = []
    
    for rank_key in world_rank_2018_dict:
        for _university in university_list:
            if rank_key == _university['world_rank_2018']:
                world_rank_2018_dict[rank_key].append(_university['university_name'])

    # pprint.pprint(world_rank_2018_dict)
    return world_rank_2018_dict

# analysis_university_rank_2018 = analyse_university_by_world_rank_2018(top_universities)
# print(analysis_university_rank_2018)


# Task 3
def analyse_university_by_country(university_list):
    university_by_country = {}
    for university in university_list:
        country = university['country']
        university_by_country[country] = []
    
    for country_key in university_by_country:
        for _university in university_list:
            if country_key == _university['country']:
                university_by_country[country_key].append(_university['university_name'])

    # pprint.pprint(university_by_country)
    return university_by_country

# analysis_university_by_country = analyse_university_by_country(top_universities)
# print(analysis_university_by_country)



# Task 4
def scrape_university_details(university_url):
    page = requests.get(university_url)
    soup = BeautifulSoup(page.text,'html.parser')
    try:
        university_name = soup.find('div',class_='institution-info__header-info').h1.get_text().strip()
        university_address = soup.find('div',class_='institution-info__contact-details-left').get_text().split('\n')

        university_ranking_div = soup.find('div',class_='rankings-score')
        world_university_rank_2019 = university_ranking_div.find('span').get_text()


        institution_courses = soup.find('div',class_='panel-pane pane-institution-courses')
        courses_list = institution_courses.find_all('li')

        university_courses_list = []
        for name in courses_list:
            courses_dict ={'course_name':'','subjects':''}
            try:
                course_name = name.find('h3').get_text()
                courses_dict['course_name'] = course_name
            except AttributeError:
                pass
        
            subjects_list = name.find_all('li')
            subjects = [subject.get_text() for subject in subjects_list]
            courses_dict['subjects'] = subjects

            if courses_dict['course_name'] != '':
                university_courses_list.append(courses_dict)

        university_details_dict = {'name':'','address':'','world_university_rank_2019':'','university_courses':''}
        university_details_dict['name'] = university_name
        university_details_dict['address'] = ' '.join(university_address).strip()
        university_details_dict['world_university_rank_2019'] = world_university_rank_2019
        university_details_dict['university_courses'] = university_courses_list

        # pprint.pprint(university_details_dict)
        return university_details_dict

    except AttributeError:
        pass

# university_details = scrape_university_details(top_universities[0]['university_url'])
# print(university_details)

# Task 5
def get_university_details(university_list):
    universities_details_list = []
    for university in university_list:
        university_url = university['university_url']
        get_details = scrape_university_details(university_url)
        universities_details_list.append(get_details)
        print(get_details)
    return universities_details_list

# universities_details = get_university_details(top_universities)
# print(universities_details)


