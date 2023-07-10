url = "https://www.rera.delhi.gov.in/"

choose = int(input('''
1. Real Estate Agents
2. Projects
'''))
new_choose = ""
if choose == 1:
    pass
else:
    new_choose = int(input('''
1. Completed Projects
2. List of Registered Projects
'''))

from selenium import webdriver
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
#REQUIRED FOR HEADLESS PART 1
from selenium.webdriver.chrome.options import Options
#REQUIRED FOR HEADLESS
from selenium.webdriver.chrome.service import Service
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains
import csv
import os
#Set location of Chrome Driver
s = Service('chromedriver.exe')
import json
#Set some selenium chrome options
chromeOptions = Options()
chromeOptions.headless = False
driver = webdriver.Chrome(service=s, options=chromeOptions)
driver.maximize_window()


def check_json(name):
    file_name = os.listdir(os.getcwd())
    if f"{name}.json" in file_name:
        pass
    else:
        new_data_dump = json.dumps([], indent=4)
        with open(f"{name}.json", "w") as outfile:
            outfile.write(new_data_dump)

def agent_data(url):
    check_json("agent_data")
    driver.get(url)
    a = ActionChains(driver)
    m= driver.find_element(By.ID, "menu-1567-1")
    a.move_to_element(m).perform()
    new_link = driver.find_element(By.ID, "menu-1572-1").find_element(By.TAG_NAME, "a").get_attribute("href") + "/" + "?combine=&items_per_page=All"
    driver.get(new_link)
    time.sleep(2)
    all_data = driver.find_element(By.CLASS_NAME, "view-content").find_element(By.CLASS_NAME, "views-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    

    for data in all_data:
        real_estate_agent_name = data.find_element(By.XPATH, "td[3]").text.splitlines()
        contact_details = data.find_element(By.XPATH, "td[4]").text.splitlines()
        registration_details = data.find_element(By.XPATH, "td[6]").text.splitlines()
        name = "None"
        designation = "None"
        name_of_person = "None"
        registered_address = "None"
        pin_code = "None"
        phone_number = "None"
        email_Id = "None"
        agent_type = data.find_element(By.XPATH, "td[5]").text
        registration_no = "None"
        valid_until = "None"
        certificate = "None"

        for registration in registration_details:
            if "Registration No. :" in registration:
                registration_no = registration[len("Registration No. :")::].strip()
            elif "Valid Until :" in registration:
                valid_until = registration[len("Valid Until :")::].strip()
            elif "Certificate :" in registration:
                certificate = data.find_element(By.XPATH, "td[6]").find_element(By.TAG_NAME, "a").get_attribute("href")

        for agent_name in real_estate_agent_name:
            if "Name :" in agent_name:
                name = agent_name[7::].strip()
            elif "Designation :" in agent_name:
                designation = agent_name[14::].strip()
            elif "Name of person :" in agent_name:
                name_of_person = agent_name[len("Name of person :")::].strip()

        for detail in contact_details:
            if "Registered Address :" in detail:
                registered_address = detail[len("Registered Address :")::].strip()
            elif "Phone Number :" in detail:
                phone_number = detail[len("Phone Number :")::].strip()
            elif "Email Id :" in detail:
                email_Id = detail[len("Email Id :")::].strip()
        
        try:
            pin_code = int(registered_address[-6::])
        except:
            pin_code = pin_code

        excel_col = ["Name", "Designation", "Name of person", "Registered Address", "Pin Code", "Phone Number", "Email Id", "Agent Type", "Registration No", "Valid Until", "Certificate"]
        excel_row = [name, designation, name_of_person, registered_address, pin_code, phone_number, email_Id, agent_type, registration_no, valid_until, certificate]
        excel_data = dict(map(lambda i,k: (i,k), excel_col, excel_row))
        
        file_name = os.listdir(os.getcwd())
        def is_url(json_name, pro_name):
            url_is = False

            if f"{json_name}.json" in file_name:
                with open(f"{json_name}.json", "r") as json_file:
                    data = json.load(json_file)
                    if len(data):
                        for new_data in data:
                            if new_data['Registration No'] == pro_name:
                                url_is = True
            else:
                new_data_dump = json.dumps([], indent=4)
                with open(f"{json_name}.json", "w") as outfile:
                    outfile.write(new_data_dump)
                    outfile.close()
            return url_is
        
        fi_name = "agent_data"
        if is_url(fi_name, registration_no):
            pass
        else:
            try:
                with open('Dellhi RERA Agent Data Sample.csv', 'r'):
                    exists = 1
            except:
                exists = 0
            # Feeding data into the current inventory_csv file
            with open('Dellhi RERA Agent Data Sample.csv', 'a', newline='', encoding="utf-8") as output_csv:
                csv1_fields = excel_col
                csv_writer = csv.DictWriter(output_csv, fieldnames=csv1_fields)
                if exists == 0:
                    csv_writer.writeheader()
                csv_writer.writerow(excel_data)
            
            json_object = ''
            with open("agent_data.json", 'r') as json_file:
                data = json.load(json_file)
                json_data = {
                    'Name': name,
                    'Registration No': registration_no,
                }
                data.append(json_data)
                # Serializing json
                json_object = json.dumps(data, indent=4)

            # Writing to sample.json
            with open("agent_data.json", "w") as outfile:
                outfile.write(json_object)


def CompletedProjects(url):
    check_json("complete_projects")
    driver.get(url)
    a = ActionChains(driver)
    m= driver.find_element(By.ID, "menu-1566-1")
    a.move_to_element(m).perform()
    new_link = driver.find_element(By.ID, "menu-1837-1").find_element(By.TAG_NAME, "a").get_attribute("href") + "/" + "?combine=&items_per_page=All"
    driver.get(new_link)
    time.sleep(2)
    all_data = driver.find_element(By.CLASS_NAME, "view-content").find_element(By.CLASS_NAME, "views-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    for data in all_data:
        promoter_details = data.find_element(By.XPATH, "td[2]").text.splitlines()
        project_details = data.find_element(By.XPATH, "td[3]").text.splitlines()
        registration_details = data.find_element(By.XPATH, "td[5]").text.splitlines()

        promoter_name = "None"
        address = "None"
        builder_pic_code = "None"
        email = "None"
        phone_number = "None"
        name = "None"
        location = "None"
        project_pin_code = "None"
        construction_status = data.find_element(By.XPATH, "td[4]").text
        registration_no = "None"
        valid_until = "None"
        certificate = "None"
        for details in promoter_details:
            if "Name :" in details:
                promoter_name = details[len("Name :")::].strip()
            elif "Address :" in details:
                address = details[len("Address :")::].strip()
            elif "Email :" in details:
                email = details[len("Email :")::].strip()
            elif "Phone Number :" in details:
                phone_number = details[len("Phone Number :")::].strip()

        try:
            builder_pic_code = int(address[-6::])
        except:
            builder_pic_code = builder_pic_code

        for project in project_details:
            if "Name :" in project:
                name = project[len("Name :")::].strip()
            elif "Location :" in project:
                location = project[len("Location :")::].strip()

        try:
            project_pin_code = int(location[-6::])
        except:
            project_pin_code = project_pin_code

        for registration in registration_details:
            if "Registration No. :" in registration:
                registration_no = registration[len("Registration No. :")::].strip()
            elif "Valid Until :" in registration:
                valid_until = registration[len("Valid Until :")::].strip()
            elif "Construction Status:" in registration:
                construction_status = registration[len("Construction Status:")::].strip()
            elif "Certificate:" in registration:
                certificate = data.find_element(By.XPATH, "td[5]").find_element(By.TAG_NAME, "a").get_attribute("href")
        
        excel_col = ["Promoter Name", "Address", "Builder Pin Code", "Email", "Phone Number", "Name", "Location", "Project Pin Code", "Registration No.", "Valid Until", "Construction Status", "Certificate"]
        excel_row = [promoter_name, address, builder_pic_code, email, phone_number, name, location, project_pin_code, registration_no, valid_until, construction_status, certificate]

        csv_data = dict(map(lambda i,j: (i,j), excel_col, excel_row))

        file_name = os.listdir(os.getcwd())
        def is_url(json_name, pro_name):
            url_is = False

            if f"{json_name}.json" in file_name:
                with open(f"{json_name}.json", "r") as json_file:
                    data = json.load(json_file)
                    if len(data):
                        for new_data in data:
                            if new_data['Registration No'] == pro_name:
                                url_is = True
            else:
                new_data_dump = json.dumps([], indent=4)
                with open(f"{json_name}.json", "w") as outfile:
                    outfile.write(new_data_dump)
                    outfile.close()
            return url_is
        
        fi_name = "complete_projects"
        if is_url(fi_name, registration_no):
            pass
        else:
            try:
                with open('Completed Projects.csv', 'r'):
                    exists = 1
            except:
                exists = 0
            # Feeding data into the current inventory_csv file
            with open('Completed Projects.csv', 'a', newline='', encoding="utf-8") as output_csv:
                csv1_fields = excel_col
                csv_writer = csv.DictWriter(output_csv, fieldnames=csv1_fields)
                if exists == 0:
                    csv_writer.writeheader()
                csv_writer.writerow(csv_data)

            json_object = ''
            with open("complete_projects.json", 'r') as json_file:
                data = json.load(json_file)
                json_data = {
                    'Name': name,
                    'Registration No': registration_no,
                }
                data.append(json_data)
                # Serializing json
                json_object = json.dumps(data, indent=4)

            # Writing to sample.json
            with open("complete_projects.json", "w") as outfile:
                outfile.write(json_object)


def RegisteredProjects(url):
    check_json("registered_projects")
    driver.get(url)
    a = ActionChains(driver)
    m= driver.find_element(By.ID, "menu-1566-1")
    a.move_to_element(m).perform()
    new_link = driver.find_element(By.ID, "menu-1575-1").find_element(By.TAG_NAME, "a").get_attribute("href") + "/" + "?combine=&items_per_page=All"
    driver.get(new_link)
    time.sleep(2)
    all_data = driver.find_element(By.CLASS_NAME, "view-content").find_element(By.CLASS_NAME, "views-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    for data in all_data:
        promoter_details = data.find_element(By.XPATH, "td[2]").text.splitlines()
        project_details = data.find_element(By.XPATH, "td[3]").text.splitlines()
        registration_details = data.find_element(By.XPATH, "td[4]").text.splitlines()

        promoter_name = "None"
        address = "None"
        builder_pic_code = "None"
        email = "None"
        phone_number = "None"
        name = "None"
        location = "None"
        project_pin_code = "None"
        registration_no = "None"
        valid_until = "None"
        certificate = "None"
        extension_certificate = "None"
        for details in promoter_details:
            if "Name :" in details:
                promoter_name = details[len("Name :")::].strip()
            elif "Address :" in details:
                address = details[len("Address :")::].strip()
            elif "Email :" in details:
                email = details[len("Email :")::].strip()
            elif "Phone Number :" in details:
                phone_number = details[len("Phone Number :")::].strip()

        try:
            builder_pic_code = int(address[-6::])
        except:
            builder_pic_code = builder_pic_code

        for project in project_details:
            if "Name :" in project:
                name = project[len("Name :")::].strip()
            elif "Location :" in project:
                location = project[len("Location :")::].strip()

        try:
            project_pin_code = int(location[-6::])
        except:
            project_pin_code = project_pin_code

        for registration in registration_details:
            if "Registration No. :" in registration:
                registration_no = registration[len("Registration No. :")::].strip()
            elif "Extension Certificate:" in registration:
                extension_certificate = registration[len("Extension Certificate:")::].strip()
            elif "Valid Until :" in registration:
                valid_until = registration[len("Valid Until :")::].strip()
            elif "Construction Status:" in registration:
                construction_status = registration[len("Construction Status:")::].strip()
            elif "Certificate:" in registration:
                certificate = data.find_element(By.XPATH, "td[5]").find_element(By.TAG_NAME, "a").get_attribute("href")
        
        excel_col = ["Promoter Name", "Address", "Builder Pin Code", "Email", "Phone Number", "Name", "Location", "Project Pin Code", "Registration No.", "Valid Until", "Construction Status", "Certificate", "Extension Certificate"]
        excel_row = [promoter_name, address, builder_pic_code, email, phone_number, name, location, project_pin_code, registration_no, valid_until, construction_status, certificate, extension_certificate]

        csv_data = dict(map(lambda i,j: (i,j), excel_col, excel_row))

        file_name = os.listdir(os.getcwd())
        def is_url(json_name, pro_name):
            url_is = False

            if f"{json_name}.json" in file_name:
                with open(f"{json_name}.json", "r") as json_file:
                    data = json.load(json_file)
                    if len(data):
                        for new_data in data:
                            if new_data['Registration No'] == pro_name:
                                url_is = True
            else:
                new_data_dump = json.dumps([], indent=4)
                with open(f"{json_name}.json", "w") as outfile:
                    outfile.write(new_data_dump)
                    outfile.close()
            return url_is
        
        fi_name = "registered_projects"
        if is_url(fi_name, registration_no):
            pass
        else:
            try:
                with open('Registered Projects.csv', 'r'):
                    exists = 1
            except:
                exists = 0
            # Feeding data into the current inventory_csv file
            with open('Registered Projects.csv', 'a', newline='', encoding="utf-8") as output_csv:
                csv1_fields = excel_col
                csv_writer = csv.DictWriter(output_csv, fieldnames=csv1_fields)
                if exists == 0:
                    csv_writer.writeheader()
                csv_writer.writerow(csv_data)
            
            json_object = ''
            with open("registered_projects.json", 'r') as json_file:
                data = json.load(json_file)
                json_data = {
                    'Name': name,
                    'Registration No': registration_no,
                }
                data.append(json_data)
                # Serializing json
                json_object = json.dumps(data, indent=4)

            # Writing to sample.json
            with open("registered_projects.json", "w") as outfile:
                outfile.write(json_object)


if choose == 1:
    agent_data(url)
else:
    if new_choose == 1:
        CompletedProjects(url)
    else:
        RegisteredProjects(url)

