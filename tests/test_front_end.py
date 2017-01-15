import unittest
import urllib2

from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import create_app, db
from app.models import Employee

# Set test variables for admin user
admin_username = "admin"
admin_email = "admin@email.com"
admin_password = "adminPASSWORD2016"

# Set test variables for test user
test_fname = "Test"
test_lname = "User"
test_username = "test"
test_email = "test@email.com"
test_password = "testPASSWORD2016"

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


class CreateObjects(object):
    def create_users(self):
        """Create the test users"""

        db.create_all()

        # create test admin user
        admin = Employee(username=admin_username,
                         email=admin_email,
                         password=admin_password,
                         is_admin=True)

        # create test non-admin user
        employee = Employee(username=test_username,
                            first_name=test_fname,
                            last_name=test_lname,
                            email=test_email,
                            password=test_password)

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def login_admin_user(self):
        """Log in as the test user"""
        login_link = self.get_server_url() + url_for('auth.login')
        self.driver.get(login_link)
        self.driver.find_element_by_id("email").send_keys(admin_email)
        self.driver.find_element_by_id("password").send_keys(admin_password)
        self.driver.find_element_by_id("submit").click()

    def login_test_user(self):
        """Log in as the test user"""
        login_link = self.get_server_url() + url_for('auth.login')
        self.driver.get(login_link)
        self.driver.find_element_by_id("email").send_keys(test_email)
        self.driver.find_element_by_id("password").send_keys(test_password)
        self.driver.find_element_by_id("submit").click()


class TestBase(LiveServerTestCase, CreateObjects):

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
        """Setup the test driver and create objects"""
        self.driver = webdriver.Chrome()
        self.create_users()

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
