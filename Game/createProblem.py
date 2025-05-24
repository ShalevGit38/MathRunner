import google.generativeai as genai
import random

genai.configure(api_key="")

model = genai.GenerativeModel('gemini-1.5-flash')

equations = []

def getEquations(len):
    response = model.generate_content(
        f" {random.randint(1, 100)} generate a list ({len}) equations of sixth grade math, without x, without any = > < signs, (÷ for /, × for multiply, - for minus, + for plus), without space, at a random order with (), when there is multiply show the symbol, between any equation put ?, dont say anything but the equations and ?"
    )
    return response.text

def createList(len):
    global equations
    equations = getEquations(len).replace("\n", "").split("?")
