import google.generativeai as genai
import random

genai.configure(api_key="hhh")

model = genai.GenerativeModel('gemini-1.5-flash')

def getEquation():
    response = model.generate_content(
        f" {random.randint(1, 100)} generate a list of (100) fifth grade math equation, without x, without any = > < signs, (÷ for /, × for multiply, - for minus, + for plus), without space, at a random order with (), when there is multiply show the symbol, between any equation put ?, dont say anything but the equations and ?"
    )
    return response.text

equations = getEquation().replace("\n", "").split("?")
print(equations)