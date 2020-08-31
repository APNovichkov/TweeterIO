def cowsay(input_string):
    """Return ASCI art of a cow saying the input_string."""

    output_string = " "

    for letter in list(input_string):
        output_string += "_"
    output_string += "__\n< {} >\n ".format(input_string)
    for letter in list(input_string):
        output_string += "-"
    output_string += "--\n"

    output_string += ("        \   ^__^\n" +
"         \  (oo)\_______\n" +
"            (__)\       )\/\\\n" +
"                ||----w |\n" +
"                ||      |\n")

    return output_string


if __name__ == "__main__":
    sample_string = "hello how are you :)"

    print(cowsay(sample_string))
