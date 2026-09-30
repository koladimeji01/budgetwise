from app.logging_config import logger


def send_email(
    recipient: str,
    subject: str,
    body: str
):
    """
    Prepare and send an email.

    The actual email provider will be connected later.
    """

    logger.info(
        f"Email prepared for {recipient}: {subject}"
    )

    return {
        "recipient": recipient,
        "subject": subject,
        "body": body
    }


def send_welcome_email(
    recipient: str,
    name: str
):
    """
    Prepare a welcome email for a new BudgetWise user.
    """

    subject = "Welcome to BudgetWise"

    body = f"""
Hello {name},

Welcome to BudgetWise!

Your account has been created successfully.

You can now use BudgetWise to:

- Track your expenses
- Monitor your spending
- View your financial dashboard
- Calculate your savings rate

Thank you for choosing BudgetWise.

Best regards,

The BudgetWise Team
"""

    return send_email(
        recipient=recipient,
        subject=subject,
        body=body
    )