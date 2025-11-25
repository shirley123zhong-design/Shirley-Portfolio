from .theme_duration import find_longest_running_themes

def run_theme_duration_interaction(df):
   
    print("\n==============================")
    print(" LONGEST RUNNING LEGO THEMES ")
    print("==============================")

    top_input = input(
        "\nHow many themes do you want to display? "
        "(Press Enter for default = 10): "
    )

    if top_input.strip() == "":
        top_n = 10
        print("Using default: Top 10")
    else:
        if top_input.isdigit() and int(top_input) > 0:
            top_n = int(top_input)
        else:
            print("Invalid input, using default = 10")
            top_n = 10

    result = find_longest_running_themes(df, top_n=top_n)
    return result
