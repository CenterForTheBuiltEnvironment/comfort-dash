from playwright.sync_api import Page, expect

expect.set_options(timeout=5_000)


def test_device_not_assigned_to_user(page: Page):
    # navigate to a device that does not exist
    page.goto("about")
    expect(page.get_by_text("About page")).to_be_visible()
