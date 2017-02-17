import unittest
import urllib2
import time

from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import create_app, db
from app.models import Employee, Role, Department

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

# Set variables for test department 1
test_department1_name = "Human Resources"
test_department1_description = "Find and keep the best talent"

# Set variables for test department 2
test_department2_name = "Information Technology"
test_department2_description = "Manage all tech systems and processes"

# Set variables for test role 1
test_role1_name = "Head of Department"
test_role1_description = "Lead the entire department"

# Set variables for test role 2
test_role2_name = "Intern"
test_role2_description = "3-month learning position"


class CreateObjects(object):

    def login_admin_user(self):
        """Log in as the test employee"""
        login_link = self.get_server_url() + url_for('auth.login')
        self.driver.get(login_link)
        self.driver.find_element_by_id("email").send_keys(test_admin_email)
        self.driver.find_element_by_id("password").send_keys(
            test_admin_password)
        self.driver.find_element_by_id("submit").click()

    def login_test_user(self):
        """Log in as the test employee"""
        login_link = self.get_server_url() + url_for('auth.login')
        self.driver.get(login_link)
        self.driver.find_element_by_id("email").send_keys(test_employee1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()


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

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        self.admin = Employee(username=test_admin_username,
                              email=test_admin_email,
                              password=test_admin_password,
                              is_admin=True)

        # create test employee user
        self.employee = Employee(username=test_employee1_username,
                                 first_name=test_employee1_first_name,
                                 last_name=test_employee1_last_name,
                                 email=test_employee1_email,
                                 password=test_employee1_password)

        # create test department
        self.department = Department(name=test_department1_name,
                                     description=test_department1_description)

        # create test role
        self.role = Role(name=test_role1_name,
                         description=test_role1_description)

        # save users to database
        db.session.add(self.admin)
        db.session.add(self.employee)
        db.session.add(self.department)
        db.session.add(self.role)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


class TestRegistration(TestBase):

    def test_registration(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly, and that they will be
        redirected to the login page
        """

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
        time.sleep(1)

        # Assert that browser redirects to login page
        assert url_for('auth.login') in self.driver.current_url

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully registered" in success_message

        # Assert that there are now 3 employees in the database
        self.assertEqual(Employee.query.count(), 3)

    def test_registration_invalid_email(self):
        """
        Test that a user cannot register using an invalid email format
        and that an appropriate error message will be displayed
        """

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

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Invalid email address" in error_message

    def test_registration_confirm_password(self):
        """
        Test that an appropriate error message is displayed when the password
        and confirm_password fields do not match
        """

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
            "password-won't-match")
        self.driver.find_element_by_id("submit").click()
        time.sleep(5)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Field must be equal to confirm_password" in error_message


class TestLogin(TestBase):

    def test_login(self):
        """
        Test that a user can login and that they will be redirected to
        the homepage
        """

        # Click login menu link
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys(test_employee1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that browser redirects to dashboard page
        assert url_for('home.dashboard') in self.driver.current_url

        # Assert that welcome greeting is shown
        username_greeting = self.driver.find_element_by_id(
            "username_greeting").text
        assert "Hi, employee1!" in username_greeting

    def test_admin_login(self):
        """
        Test that an admin user can login and that they will be redirected to
        the admin homepage
        """

        # Click login menu link
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys(test_admin_email)
        self.driver.find_element_by_id("password").send_keys(
            test_admin_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that browser redirects to dashboard page
        assert url_for('home.admin_dashboard') in self.driver.current_url

        # Assert that welcome greeting is shown
        username_greeting = self.driver.find_element_by_id(
            "username_greeting").text
        assert "Hi, admin!" in username_greeting

    def test_login_invalid_email_format(self):
        """
        Test that a user cannot login using an invalid email format
        and that an appropriate error message will be displayed
        """

        # Click login menu link
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys("invalid")
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Invalid email address" in error_message

    def test_login_wrong_email(self):
        """
        Test that a user cannot login using the wrong email
        and that an appropriate error message will be displayed
        """

        # Click login menu link
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys(test_employee2_email)
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that error message is shown
        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Invalid email or password" in error_message

    def test_login_wrong_password(self):
        """
        Test that a user cannot login using the wrong password
        and that an appropriate error message will be displayed
        """

        # Click login menu link
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys(test_employee1_email)
        self.driver.find_element_by_id("password").send_keys(
            "invalid")
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that error message is shown
        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Invalid email or password" in error_message


class TestDepartments(CreateObjects, TestBase):

    def test_add_department(self):
        """
        Test that an admin user can add a department
        """

        # Login as admin user
        self.login_admin_user()

        # Click departments menu link
        self.driver.find_element_by_id("departments_link").click()
        time.sleep(1)

        # Click on add department button
        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Fill in add department form
        self.driver.find_element_by_id("name").send_keys(test_department2_name)
        self.driver.find_element_by_id("description").send_keys(
            test_department2_description)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully added a new department" in success_message

        # Assert that there are now 2 departments in the database
        self.assertEqual(Department.query.count(), 2)

    def test_add_existing_department(self):
        """
        Test that an admin user cannot add a department with a name
        that already exists
        """

        # Login as admin user
        self.login_admin_user()

        # Click departments menu link
        self.driver.find_element_by_id("departments_link").click()
        time.sleep(1)

        # Click on add department button
        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Fill in add department form
        self.driver.find_element_by_id("name").send_keys(test_department1_name)
        self.driver.find_element_by_id("description").send_keys(
            test_department1_description)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Error: department name already exists" in error_message

        # Assert that there is still only 1 department in the database
        self.assertEqual(Department.query.count(), 1)

    def test_edit_department(self):
        """
        Test that an admin user can edit a department
        """

        # Login as admin user
        self.login_admin_user()

        # Click departments menu link
        self.driver.find_element_by_id("departments_link").click()
        time.sleep(1)

        # Click on edit department link
        self.driver.find_element_by_class_name("fa-pencil").click()
        time.sleep(1)

        # Fill in add department form
        self.driver.find_element_by_id("name").clear()
        self.driver.find_element_by_id("name").send_keys("Edited name")
        self.driver.find_element_by_id("description").clear()
        self.driver.find_element_by_id("description").send_keys(
            "Edited description")
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully edited the department" in success_message

        # Assert that department name and description has changed
        department = Department.query.get(1)
        self.assertEqual(department.name, "Edited name")
        self.assertEqual(department.description, "Edited description")

    def test_delete_department(self):
        """
        Test that an admin user can delete a department
        """

        # Login as admin user
        self.login_admin_user()

        # Click departments menu link
        self.driver.find_element_by_id("departments_link").click()
        time.sleep(1)

        # Click on edit department link
        self.driver.find_element_by_class_name("fa-trash").click()
        time.sleep(1)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully deleted the department" in success_message

        # Assert that there are no departments in the database
        self.assertEqual(Department.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
