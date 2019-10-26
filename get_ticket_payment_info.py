import datetime


def get_ticket_payment_info():
    tno = get_tno()
    pdate = get_pdate().strftime("%Y-%m-%d")
    amount = get_amount()

    return tno, pdate, amount


def get_tno():
    tno = input("Enter the ticket number: ")
    return tno


def get_pdate():
    pdate = datetime.date.today()
    return pdate


def get_amount():
    amount = input("Enter the payment amount: ")
    while True:
        try:
            int(amount)
            break
        except ValueError:
            amount = input("Enter the payment amount: ")

    return amount
