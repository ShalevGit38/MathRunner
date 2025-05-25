import google.generativeai as genai
import random

genai.configure(api_key="9ZId7eBuRw")

model = genai.GenerativeModel('gemini-1.5-flash')

equations = []

def getEquations(len):
    global equations
    
    response = model.generate_content(
        f" {random.randint(1, 100)} generate a list ({len}) equations of sixth grade math, without x, without any = > < signs, (÷ for /, × for multiply, - for minus, + for plus), without space, at a random order with (), when there is multiply show the symbol, between any equation put ?, dont say anything but the equations and ?"
    )
    equations = response.text
    equations = equations.replace("\n", "").split("?")
