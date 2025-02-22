import google.generativeai as genai

class GeminiModel:
    def initGeminiModel(apiKey: str):
        genai.configure(api_key=apiKey)
        return genai.GenerativeModel("gemini-1.5-flash")

    def getGeminiQuery(model: genai.GenerativeModel, companyDetails: str):
        query = (
        f'Details (description) about the company is provided in quatation marks. Language is Lithuanian.' 
        f'Summarize the details in maximum 2 sentences and preserve all the important information about the company. Use Lithuanian language /n/n'
        f'"{companyDetails}"'
        )

        response = model.generate_content(query)
        # print(response.text)
        return response.text
