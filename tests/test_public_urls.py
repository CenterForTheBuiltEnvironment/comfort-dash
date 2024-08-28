from playwright.sync_api import Page, expect

expect.set_options(timeout=5_000)


def test_home_page_text_visible(page: Page):
    page.goto("/")

    # Expect a title "to contain" a substring.
    expect(page.get_by_text("Select model")).to_be_visible()
    expect(page.get_by_text("Inputs")).to_be_visible()


def test_about_page(page: Page):
    # navigate to a device that does not exist
    page.goto("about")
    expect(page.get_by_text("About page")).to_be_visible()
