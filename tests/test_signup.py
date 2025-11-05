import os
from typing import Optional

import pytest
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from tigrmail import Tigrmail, TigrmailError

load_dotenv()

TIGRMAIL_TOKEN: Optional[str] = os.getenv("TIGRMAIL_TOKEN")


def extract_first_link(html: str) -> Optional[str]:
    """Return the first <a> href from an HTML payload, if present."""
    soup = BeautifulSoup(html, "html.parser")
    first_anchor = soup.find("a")
    return first_anchor.get("href") if first_anchor else None


@pytest.mark.skipif(not TIGRMAIL_TOKEN, reason="Set TIGRMAIL_TOKEN in .env")
def test_user_can_sign_up_and_verify_email(page: Page) -> None:
    if not TIGRMAIL_TOKEN:
        pytest.fail("Set TIGRMAIL_TOKEN in .env")

    tigr = Tigrmail(token=TIGRMAIL_TOKEN)
    try:
        email_address = tigr.create_email_address()

        page.goto("/sign-up")
        page.get_by_test_id("email-input").fill(email_address)
        page.get_by_test_id("password-input").fill("TestPassword123!")
        page.get_by_test_id("password-confirm-input").fill("TestPassword123!")
        page.get_by_test_id("submit-btn").click()

        expect(page.get_by_test_id("verification-status")).to_have_text(
            "Your email is not verified. Please check your inbox for the verification email."
        )

        message = tigr.poll_next_message(inbox=email_address)
        verification_link = extract_first_link(message["body"])
        if not verification_link:
            pytest.fail("No <a> href found in the email body")

        page.goto(verification_link)
        page.wait_for_selector("text=Your email has been verified")
        page.go_back()

        expect(page.get_by_test_id("verification-status")).to_have_text("Your email is verified!")
    except TigrmailError as exc:
        pytest.fail(f"Tigrmail SDK error: {exc}")
    finally:
        tigr.close()
