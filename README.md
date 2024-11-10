# Big Data Programming: Lab Management System

this project is also hosted on this URL and can be easily accessed for all types of evaluations: 	[https://labsystem.pythonanywhere.com	](https://labsystem.pythonanywhere.com)

# Group Members

1. **Usman Shahid (L1F22BSCS1057)**
2. **Ahmad Sohail (L1F22BSCS1048)**
3. **Anas Yousaf (L1F22BSCS1070)**

# Submitted To.

**Ms. Misbah Naz**

# Project Setup and installation:

**For `windows` use the following procedure:**

Download and install the latest version of python from https://python.org

Download the project file in .zip format or clone the repository

Use this command for git bash to clone this github repo: `git clone https://github.com/usman-s-mahmood/medical-lab-system-in-django`

In the folder where you have extracted the files, open powershell by using `shift+right-click`

In powershell type this command for the creation of virtual environment: `python -m venv virt`

The type this command to activate disabled scripts: `set-ExecutionPolicy unrestricted -scope currentuser -force`

After that use this command to activate the virtual environment `cd virt/scripts; ./Activate.ps1; cd ..; cd ..;`

After that cd into the project directory and use the command `pip install -r requirements.txt` to install the required dependencies and libraries

Use this command `python manage.py runserver` to run the project on local machine

**For Installation in `linux` follow these steps:**

Clone the repository to your local machine

Use `sudo apt install python` to install python

Use `sudo python3 -m venv virt` to create a virtual environment with the name virt

To activate the virtual environment, use the command `sudo source virt/bin/activate`

Once the virtual environment is activated then install the required dependencies by navigating into the folder of project and using the command `pip install -r requirements.txt`

After installing the dependencies use this command to run the web app: `python manage.py runserver`

<hr>

**This project demonstrates the automation of medical lab system that allows individuals to access their medical reports online. The website serves as a CRM with extensive features for data analysis of medical reports through an excel file that contatins the result score of patients and their personal information.**

---

**All the data is securely kept in the websites database and only the actual owner of the medical report can access the data of report. User reports are distingueshed by the unique email provided by the user at the time of test and multiple checks are placed to counter email uniqueness of the users**

# Technical Details and Framework Details

**The website uses a bootstrap front end that is a light utility of javascript and CSS for developing stunning mobile responsive web application**

**The backend of this website is powered by django framework and uses pandas for data analysis of excel spread sheet containing the records of patients**

**Reportlab library is used for generating PDF reports of users containing all the details about the test and evaluation of patient**

**The web app also provides the facility of sample dataset generation for training of employees. Employee can provide the size of dataset that is to be generated and the an excel file will be created and made available to the user for dowloading. The excel file contains columns with synthetic data that does not belong to any real person in the world and randomly generates test results**

---

# Frameworks and Libraries used in this project

| Framework      | Usage in project                                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Django         | For robust user authentication and granular backend control                                                                        |
| Pandas         | For reading dataset and producing sample dataset                                                                                   |
| Reportlab      | For making PDF reports                                                                                                             |
| Faker          | For synthetic data generation. This synthetic data does not belong to any real world person                                        |
| Gender Guesser | For guessing gender of patient with respect to their name, used in case of dataset generation only                                 |
| Numpy          | For memory effective handling of array based data                                                                                  |
| Gunicorn       | For deploying project on hosting platform. It allows the project to use complete CPU and RAM power for wsgi based web applications |

# Web Application Structure and File System

This CRM based website consists of 3 Applications (AuthApp, BlogApp, LabApp).

For development purposes, sqlite3 database is used in the project for handling data of users.

Two public folders are used in this application for management of static files and reports

Report files are kept in media/reports folder while the dataset uploaded for analysis is stored in media/reports/uploads folder. Whenever a user generates a sample dataset then it is also stored locally on the web app to keep a track of the user who generated the dataset. Location for saving the dataset is media/reports/sample. Client/Patient Reports are kept in media/reports/clients folder

The main driver code for these three apps are in the views.py file of each app

AuthApp/views.py contians all the functions related to user authentication like login, logout, user_dashboard, user_editing, profile_creation, user_registrations, etc.

BlogApp/views.py contains all the functions related to content management and blogging for the end beneficiaries.

LabApp/views.py contains the core configuration of this project and it has 2 functions that are mainly performing most of the task. The first function is for generating a sample dataset with .xlsx extension that is for demonstration purposes only so that management can understand what type of input this app is intended to handle. The second function is for the analysis of excel file as a dataset that provides information about patient like name, gender, email, phone number, date of birth, test type, payment, payment status and test score. This information within the file is used to evaluate either the patient is positive or negative and save the results of patient within a database along with a PDF file.

*The idea for this web application is that it allows the medical lab management to analyze the medical info of patients and save the results in database, if a user(patient) intends to see their report then they would have to register with an account on the website and they would have to provide the same email that they provided to reception before their test conduction because this email would be used to uniquely identify the reports of patients. As soon as the patient registers on the application, they will be redirected to their dashboard where they can access their reports if their registered email matches and the payment status is paid*

to see the working of this web application you can use the account with username: test.user password: patient123. By logging into this web app with this account, you can see how patient reports are displayed to the user

for admin level access there is a file within this submission folder named "admin_user_account.txt" that can be used to access the admin account of this website and see how things are done at management level in this web application
