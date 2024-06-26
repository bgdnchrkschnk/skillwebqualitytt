import time

import pytest
from playwright.sync_api import Page, expect
from faker import Faker
from allure import title, description, suite, severity, severity_level, attach, attachment_type


faker = Faker()


class TestRegistrationForm:
    TEMPMAIL_URL: str = "https://tempail.com/ua/"
    BASE_URL: str = "https://first.ua/"
    CURRENT_EMAIL: str = None
    CURRENT_PW: str = None

    @title("Registration with empty fields")
    @description("Verify that system shows error message if user registers with empty fields")
    @severity(severity_level.NORMAL)
    @suite("Registration form testing")
    def test_empty_fields(self, s_page: Page):
        s_page.goto(url=self.BASE_URL + "ua/auth/signup")
        time.sleep(1)
        s_page.get_by_text(text="Е-пошта").click()
        register_btn = s_page.locator("button[data-v-e18269df][data-v-225103f9]")
        register_btn.wait_for(timeout=30000)
        register_btn.click()
        error = s_page.get_by_text("Email обов'язковий для заповнення")
        error.wait_for()
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        expect(error).to_be_visible()

    @title("Registration underage user")
    @description("Verify that system does not allow to register for underage user")
    @severity(severity_level.NORMAL)
    @suite("Registration form testing")
    def test_register_underage(self, s_page: Page):
        self.__class__.CURRENT_EMAIL = faker.free_email()
        self.__class__.CURRENT_PW = faker.password(length=8, digits=True, lower_case=True, upper_case=True,
                                                   special_chars=True)
        email_field = s_page.locator("input[type=email]")
        pw_field = s_page.locator("input[type=password]")
        email_field.type(text=self.__class__.CURRENT_EMAIL, delay=100)
        pw_field.type(text=self.__class__.CURRENT_PW, delay=100)
        age_checkbox = s_page.locator("div.ui-checkbox.is-active.type-primary")
        age_checkbox.click()
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        expect(s_page.locator("button[data-v-e18269df][data-v-225103f9]")).to_have_class(
            "is-disabled is-block is-primary-accent is-m-size is-center-justify ui-button")

    @title("Registration with invalid email format")
    @description("Verify that system does not allow to register with invalid email format")
    @severity(severity_level.NORMAL)
    @suite("Registration form testing")
    @pytest.mark.parametrize("email", ["hjbdhsjv.gmail.com","feubub@gmail","snefkj@@gmail.com"])
    def test_register_invalid_email_format(self, email, s_page: Page):
        s_page.goto(url=self.BASE_URL + "ua/auth/signup")
        s_page.get_by_text(text="Е-пошта").click()
        email_field = s_page.locator("input[type=email]")
        email_field.wait_for()
        pw_field = s_page.locator("input[type=password]")
        pw_field.wait_for()
        email_field.fill(email)
        pw_field.fill(self.__class__.CURRENT_PW)
        register_btn = s_page.locator("button[data-v-e18269df][data-v-225103f9]")
        register_btn.wait_for(timeout=30000)
        register_btn.click()
        error = s_page.get_by_text("НЕВІРНА АДРЕСА ЕЛЕКТРОННОЇ ПОШТИ")
        error.wait_for()
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        expect(error).to_be_visible()

    @title("Registration with existing email")
    @description("Verify that system does not allow to register with existing email in system")
    @severity(severity_level.CRITICAL)
    @suite("Registration form testing")
    def test_register_existing_email(self, s_page: Page):
        s_page.goto(url=self.BASE_URL + "ua/auth/signup")
        s_page.get_by_text(text="Е-пошта").click()
        email_field = s_page.locator("input[type=email]")
        email_field.wait_for()
        pw_field = s_page.locator("input[type=password]")
        pw_field.wait_for()
        email_field.fill(value="bgdnchrkschnk@gmail.com")
        pw_field.fill(self.__class__.CURRENT_PW)
        register_btn = s_page.locator("button[data-v-e18269df][data-v-225103f9]")
        register_btn.wait_for(timeout=30000)
        register_btn.click()
        error = s_page.get_by_text("ТАКИЙ КОРИСТУВАЧ ВЖЕ ІСНУЄ")
        error.wait_for()
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        expect(error).to_be_visible()

    @title("Mask/Unmask password field")
    @description("Verify that mask/unmask pw field works correctly")
    @severity(severity_level.NORMAL)
    @suite("Registration form testing")
    def test_mask_password(self, s_page: Page):
        s_page.goto(url=self.BASE_URL + "ua/auth/signup")
        s_page.get_by_text(text="Е-пошта").click()
        pw_field = s_page.locator("input[type=password]")
        pw_field.wait_for()
        pw_field.type(self.__class__.CURRENT_PW, delay=100)
        s_page.locator("button.show-password-button").click()
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        expect(s_page.locator("input[data-rr-is-password]")).to_have_attribute(name="type", value="text")

    @title("Registration with incorrect password format")
    @description("Verify that system does not allow to register with incorrect password format")
    @severity(severity_level.NORMAL)
    @suite("Registration form testing")
    @pytest.mark.parametrize("password", ["1","fes","//*"])
    def test_register_invalid_password_format(self, password, s_page: Page):
        s_page.goto(url=self.BASE_URL + "ua/auth/signup")
        s_page.get_by_text(text="Е-пошта").click()
        email_field = s_page.locator("input[type=email]")
        email_field.wait_for()
        pw_field = s_page.locator("input[type=password]")
        pw_field.wait_for()
        email_field.fill(self.__class__.CURRENT_EMAIL)
        pw_field.fill(password)
        register_btn = s_page.locator("button[data-v-e18269df][data-v-225103f9]")
        register_btn.wait_for(timeout=30000)
        register_btn.click()
        error = s_page.get_by_text("ЦЕЙ ПАРОЛЬ НЕ ПІДХОДИТЬ АБО ВІН МІСТИТЬ ПОМИЛКУ")
        error.wait_for()
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        expect(error).to_be_visible()
