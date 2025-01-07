import google.generativeai as genai

class GeminiModel:
    def initGeminiModel():
        genai.configure(api_key="AIzaSyCKhoUdsFUWxA0UrjTzMgE7ALbQQakSC1g")
        return genai.GenerativeModel("gemini-1.5-flash")

    def getGeminiQuery(model: genai.GenerativeModel, competitorData: str):
        query = (
        f'Details about company are provided in quatation marks. The text is not clean. Clean the text and make a summary from the provided text.' 
        f'If there are any news about the company, list them with exact headlines or if they dont have headlines summarize the news into headline making a list of them.'
        f'"{competitorData}"'
        )

        response = model.generate_content(query)
        print(response.text)
        return response.text
