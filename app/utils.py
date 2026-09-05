def get_valid_amount(prompt):

    while True:

        try:

            amount = float(input(prompt))

            if amount <= 0:
                print(
                    "Amount must be greater than zero."
                )
                continue

            return amount

        except ValueError:

            print(
                "❌ Invalid amount. "
                "Please enter a number."
            )


def get_valid_text(prompt):

    while True:

        value = input(prompt).strip()

        if value == "":
            print(
                "❌ This field cannot be empty."
            )
            continue

        return value


def get_valid_id(prompt):

    while True:

        try:

            value = int(input(prompt))

            if value <= 0:
                print(
                    "ID must be greater than zero."
                )
                continue

            return value

        except ValueError:

            print(
                "❌ Please enter a valid ID."
            )