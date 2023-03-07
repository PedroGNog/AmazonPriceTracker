import requests
from bs4 import BeautifulSoup
import smtplib
import email.message

# Fill in all the variables between the quotation marks including the discount price
url = "THE URL OF THE PRODUCT THAT YOU WANT TO TRACK THE PRICE"
discount_price = "THE PRICE THAT YOU WANT TO BUY THE PRODUCT (Inside the quotation marks)"
email_sender = "THE EMAIL THAT YOU WANT TO SEND FROM"
password = "THE 2 FACTOR AUTHENTICATION PASSWORD OF THE EMAIL THAT YOU WANT TO SEND FROM"
subject_title = "THE TITLE OF THE EMAIL THAT YOU WANT TO SENT"
list_to_send = ["THE LIST OF EMAILS THAT YOU WANT TO SEND TO"]

# In this variable is made the request for the content of the page
# Here in requests you have to change the User-Agent and the Accept-Language if needed
# Access https://myhttpheader.com/ to get the information to change it
req = requests.get(url=url,
                   headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                          "(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                                          "Accept-Language": "pt-BR,pt;q=0.9"}).content

# In this variable is used BeautifulSoup to make the content more likely to work with
soup = BeautifulSoup(req, "lxml")

# This variable is where with BeautifulSoup is allocated the whole of the price
price_whole = soup.find("div", id="corePrice_feature_div").find("span", class_="a-price-whole").text.strip()

# This variable is where with BeautifulSoup is allocated the fraction of the price
price_fraction = soup.find("div", id="corePrice_feature_div").find("span", class_="a-price-fraction").text.strip()

# This variable is where the parts of the price are concatenated
price = f"{price_whole[:-1]}.{price_fraction}"

# Here is where the string price is converted to a float number
price = float(price)

# This variable is the whole price with the $ in string variable
price_in_text = soup.find("div", id="corePrice_feature_div").find("span", class_="a-offscreen").text.strip()


# This variable gets the product title
product_name = soup.find("span", id="productTitle", class_="a-size-large product-title-word-break").text.strip()


# This function is for sending e-mails
def sending_alert(receiver):
    try:
        # This variable is where the message is composed
        text_body = f"{product_name} is now {price_in_text}\n{url}"
        message = email.message.Message()

        # In this variable you can enter the subject title of the email that you want to send
        message["Subject"] = subject_title

        # This variable is where the sender e-mail is placed
        message["From"] = email_sender

        # This variable is where the sender password 2-authentication is placed
        authentication_password = password

        # This variable is where the receiver e-mail is placed
        message["To"] = receiver
        message.add_header("Content-Type", "text/html")
        message.set_payload(text_body)

        # This variable is where the connexion with the smtp is made
        # Gmail - "smtp.gmail.com" / Hotmail: smtp.live.com /
        # Outlook - outlook.office365.com / Yahoo - smtp.mail.yahoo.com
        conn = smtplib.SMTP("smtp.gmail.com", 587)

        conn.starttls()

        # Here the login with the account is made
        conn.login(message["From"], authentication_password)

        # Here the email is sent in a more readable way with encode in utf-8
        conn.sendmail(message["From"], message["To"], message.as_string().encode("utf-8"))

        # Here the connection with email server is cut off
        conn.quit()

        print("Email sent")
    except Exception as ex:
        print(f"Exception: {ex}\nEmail not sent.")


# This variable receives a list of the e-mail(s) that you want to send to
receivers_list = list_to_send

if price <= float(discount_price):
    for mail in receivers_list:
        sending_alert(mail)
