import requests
from class_notification_utils import NotificationUtility

def email_joke(p_joke : str, p_email_to_list : list) -> None:
    w_message   = f"""
                Good day,

                Joke:: {p_joke} 
                
                🤣🤣🤣🤣

                Have a great one.                
                """
    notification = NotificationUtility()
    notification.send_email(p_email_to  = p_email_to_list,
                            p_subject   = "Joke of the day 😏",
                            p_message   = w_message)


def main() -> None:
    w_email_to      : str = input("Enter Email address to send joke to (comma separated if more than one): ").strip().lower().replace(";",",")
    w_email_to_list : list = [i.strip() for i in w_email_to.split(",") if i]#remove empty data

    w_respnse = requests.get("https://icanhazdadjoke.com/slack")
    w_respnse.raise_for_status()

    try:
        # print(json.dumps(w_respnse.json(), indent=4))
        w_joke_data = w_respnse.json()        
        w_joke =  w_joke_data["attachments"][0]["text"]
        print(w_joke)

        if w_joke and w_email_to_list:
            email_joke(p_joke      = w_joke, 
                    p_email_to_list = w_email_to_list)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()