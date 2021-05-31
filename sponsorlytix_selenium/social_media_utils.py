def convert_followers_to_number(number_followers_str: str, flag_full_string: bool):

    number_followers_str = number_followers_str.replace(" Followers", "")


    if flag_full_string :

        followers_str = ''

        for digit in number_followers_str:

            if digit.isdigit():

                followers_str = followers_str + digit

        number = int(followers_str)

    else:

        followers_decimals_dict = {
            "K": 3,
            "M": 6,
            "B": 9
        }

        decimal_letter = number_followers_str[-1:]
        followers_amount = number_followers_str[:-1]
        
        if not followers_amount.isdigit():
            number = int(float(followers_amount) * pow(10, followers_decimals_dict.get(decimal_letter.upper())))

        else:
            try:
                number = int(number_followers_str)
            except ValueError as e:
                raise ValueError(f"Float value without letter in the end string, value from social media: "
                                 f"{number_followers_str}, error: {e.args[0]}")

    return number
