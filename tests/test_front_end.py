import unittest
import urllib2
import time

# from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import create_app, db
from app.models import Employee

# Set test variables for test admin user
test_admin_username = "admin"
test_admin_email = "admin@email.com"
test_admin_password = "admin2016"

# Set test variables for test employee 1
test_employee1_first_name = "Test"
test_employee1_last_name = "Employee"
test_employee1_username = "employee1"
test_employee1_email = "employee1@email.com"
test_employee1_password = "1test2016"

# Set test variables for test employee 2
test_employee2_first_name = "Test"
test_employee2_last_name = "Employee"
test_employee2_username = "employee2"
test_employee2_email = "employee2@email.com"
test_employee2_password = "2test2016"

# Set variables for test departments
test_department_name = "Human Resources"
test_department_name2 = "Find and keep the best talent"
test_department_description = "Information Technology"
test_department_description2 = "Manage all tech systems and processes"

# Set variables for test roles
test_role_name = "Head of Department"
test_role_name2 = "Lead the entire department"
test_role_description = "Intern"
test_role_description2 = "3-month learning position"


# class CreateObjects(object):
#
#     def login_admin_user(self):
#         """Log in as the test employee"""
#         login_link = self.get_server_url() + url_for('auth.login')
#         self.driver.get(login_link)
#         self.driver.find_element_by_id("email").send_keys(test_admin_email)
#         self.driver.find_element_by_id("password").send_keys(test_admin_password)
#         self.driver.find_element_by_id("submit").click()
#
#     def login_test_user(self):
#         """Log in as the test employee"""
#         login_link = self.get_server_url() + url_for('auth.login')
#         self.driver.get(login_link)
#         self.driver.find_element_by_id("email").send_keys(test_email)
#         self.driver.find_element_by_id("password").send_keys(test_password)
#         self.driver.find_element_by_id("submit").click()
#
#     def create_first_department(self):
#         self.login_admin_user()
#         departments_link = self.get_server_url() + url_for('admin.')
#         self.driver.get(departments_link)


class TestBase(LiveServerTestCase):

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            # Specify the test database
            SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2016@localhost/dreamteam_test',
            # Change the port that the liveserver listens on
            LIVESERVER_PORT=8943
        )
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

        db.create_all()

        # create test admin user
        admin = Employee(username=test_admin_username,
                         email=test_admin_email,
                         password=test_admin_password,
                         is_admin=True)

        # create test employee user
        employee = Employee(username=test_employee1_username,
                            first_name=test_employee1_first_name,
                            last_name=test_employee1_last_name,
                            email=test_employee1_email,
                            password=test_employee1_password)

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


class TestAuth(TestBase):

    def test_registration(self):

        # Click register menu link
        self.driver.find_element_by_id("register_link").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_id("email").send_keys(test_employee2_email)
        self.driver.find_element_by_id("username").send_keys(
            test_employee2_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_employee2_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_employee2_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("submit").click()

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully registered" in success_message

        # Assert that there are now 3 employees in the database
        self.assertEqual(Employee.query.count(), 3)

    def test_registration_invalid_email(self):

        # Click register menu link
        self.driver.find_element_by_id("register_link").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_id("email").send_keys("invalid_email")
        self.driver.find_element_by_id("username").send_keys(
            test_employee2_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_employee2_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_employee2_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(5)

        # Assert success message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Invalid email address" in error_message

    def test_registration_confirm_password(self):

        # Click register menu link
        self.driver.find_element_by_id("register_link").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_id("email").send_keys("invalid_email")
        self.driver.find_element_by_id("username").send_keys(
            test_employee2_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_employee2_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_employee2_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            "password-won't-match")
        self.driver.find_element_by_id("submit").click()
        time.sleep(5)

        # Assert success message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Field must be equal to confirm_password" in error_message

    def test_login(self):

        # Click login menu link
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys(test_employee1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that welcome greeting is shown
        username_greeting = self.driver.find_element_by_id(
            "username_greeting").text
        assert "Hi, employee1!" in username_greeting


if __name__ == '__main__':
    unittest.main()
