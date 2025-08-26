

import argparse

color_definitions = {

        "accent-light": "#96B5CA" ,
        "accent-dark":  "#5788a9" ,
        "accent-very-dark": "#42667F",

        "background-accent-light": "  #96B5CA", 
        "background-accent-dark": "  #5788a9",
        "background-accent-very-dark": "  #42667F", 

        "background": " rgb(238,238,238)", 
        "background-test": " magenta", 
        "background-light": "rgb(238,238,238)", 
        "background-dark": " rgb(212,212,212)", 

        "shadow-light": " rgb(179,179,179)", 
        "shadow-mid": "rgb(117,117,117)", 

        "grid-light": "rgb(222,222,222)", 
        "grid-dark": "  rgb(117,117,117)", 

        "focused-light": " rgb(255,226,127)", 
        "focused-very-light": " rgb(249,208,92)", 
        "focused-dark": " rgb(229,163,47)", 
        "focused-very-dark": " rgb(157,82,11)", 
}

def main():
    parser = argparse.ArgumentParser(description="A simple script with arguments.")
    parser.add_argument("path", type=str)
    
    parser.add_argument("--use-variables",  action='store_true')
    parser.add_argument("--out", type=str, default="", help="")
    args = parser.parse_args()
    print(args)
    with open(args.path, encoding='utf-8') as inputf:

        svg_text = inputf.read()
        for key, value in color_definitions.items() :
            variable_key = f"var(--{key})"
            if not args.use_variables:
                svg_text = svg_text.replace(variable_key, value)
            else:
                svg_text = svg_text.replace(value, variable_key)
    if args.out == "" or args.out == "-":
        print(svg_text)
    else:
        with open(args.out, 'w', encoding='utf-8') as outf:
            outf.write(svg_text)

main()
