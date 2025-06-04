import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"  # измени, если у тебя другой порт/домен

@pytest.fixture
def login(page: Page):
    def do_login():
        page.goto(f"{BASE_URL}/login")
        page.fill('input[name="username"]', "Pasha")   # или другой логин
        page.fill('input[name="password"]', "123123123")   # и пароль
        page.click('button[type="submit"]')
        expect(page).to_have_url(f"{BASE_URL}/")
    return do_login


def test_load_users(page: Page, login):
    login()
    page.goto(f"{BASE_URL}/users")

    # проверяем, что таблица пользователей видна
    expect(page.locator("table")).to_be_visible()


    # Logout (если нужен)
    page.click("text=Logout")
    expect(page).to_have_url(f"{BASE_URL}/login")