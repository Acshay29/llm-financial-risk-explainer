import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class LLMRiskExplainer:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

    def generate_explanation(self, prediction: int, probability: float, customer_features: dict, shap_values: dict) -> dict:
        risk_level = "High Risk" if prediction == 1 else "Low Risk"
        
        # Prepare SHAP values for prompt
        risk_factors_str = "\n".join([f"- {f['feature']}: {f['value']} (SHAP impact: {f['shap_value']:.2f})" for f in shap_values['risk_factors']])
        positive_factors_str = "\n".join([f"- {f['feature']}: {f['value']} (SHAP impact: {f['shap_value']:.2f})" for f in shap_values['positive_factors']])

        prompt = f"""You are an AI assistant specializing in financial risk assessment. Your task is to generate a compliance-friendly explanation for a loan default risk prediction. The explanation should be structured as a JSON object and adhere to strict rules:

Input Data:
- Prediction: {prediction} (0 = No Default, 1 = Default)
- Probability of Default: {probability:.2f}
- Customer Features: {json.dumps(customer_features, indent=2)}
- Top Risk Factors (features increasing default probability):
{risk_factors_str}
- Top Positive Factors (features decreasing default probability):
{positive_factors_str}

Output JSON Structure:
{{
  "risk_level":"<High Risk/Low Risk>",
  "summary":"<Concise summary of the risk assessment>",
  "risk_factors":["<Factor 1 explanation>", "<Factor 2 explanation>"],
  "positive_factors":["<Factor 1 explanation>", "<Factor 2 explanation>"],
  "loan_officer_notes":"<Detailed notes for a loan officer, including technical details and potential follow-ups>",
  "customer_explanation":"<Simple, clear explanation for the customer>",
  "recommendations":["<Recommendation 1>", "<Recommendation 2>"]
}}

Rules for Generation:
1. Use only the supplied data. Do not hallucinate or invent information.
2. All language must be compliance-friendly, avoiding discriminatory or biased terms.
3. The 'risk_level' should be '{risk_level}'.
4. 'summary' should be a brief overview of the prediction and key drivers.
5. 'risk_factors' and 'positive_factors' should explain *why* these factors are impactful based on the provided SHAP values and customer features. Focus on the top 3-5 most impactful factors.
6. 'loan_officer_notes' should be comprehensive, detailing the model's decision, the specific features contributing to it, and any nuances. It should be suitable for internal review.
7. 'customer_explanation' should be easy to understand for a non-expert, focusing on actionable insights if possible.
8. 'recommendations' should suggest actions to mitigate risk or improve approval chances, derived directly from the identified factors.
9. Ensure the output is a valid JSON string.

Generate the JSON explanation now:
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                temperature=0.7,
            )
            explanation_json = json.loads(response.choices[0].message.content)
            return explanation_json
        except Exception as e:
            logger.error(f"Error generating LLM explanation: {e}")
            return {
                "risk_level": risk_level,
                "summary": "Error generating explanation.",
                "risk_factors": [],
                "positive_factors": [],
                "loan_officer_notes": f"Failed to generate LLM explanation due to: {e}",
                "customer_explanation": "We are unable to provide a detailed explanation at this moment.",
                "recommendations": []
            }

    def risk_analyst_copilot(self, question: str, prediction_data: dict) -> str:
        # This method will answer questions based on the prediction_data context
        # For now, a simplified implementation. This can be expanded with more sophisticated RAG or prompt engineering.
        
        prompt = f"""You are an AI assistant acting as a risk analyst copilot. Based on the provided loan prediction data, answer the following question concisely and professionally. If the information is not directly available, state that you cannot answer based on the provided data.

Loan Prediction Data:
{json.dumps(prediction_data, indent=2)}

Question: {question}

Answer:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in Risk Analyst Copilot: {e}")
            return f"An error occurred while processing your request: {e}"

if __name__ == "__main__":
    # Example usage for testing
    explainer = LLMRiskExplainer()
    
    sample_customer_features = {
        "age": 30,
        "income": 50000,
        "loan_amount": 25000,
        "credit_score": 620,
        "employment_years": 5,
        "existing_debts": 2,
        "home_ownership": "RENT",
        "loan_purpose": "DEBT_CONSOLIDATION"
    }
    
    sample_shap_values = {
        "risk_factors": [
            {"feature": "credit_score", "value": 620, "shap_value": 0.35},
            {"feature": "loan_amount", "value": 25000, "shap_value": 0.20}
        ],
        "positive_factors": [
            {"feature": "income", "value": 50000, "shap_value": -0.15},
            {"feature": "employment_years", "value": 5, "shap_value": -0.08}
        ]
    }
    
    prediction = 1 # Example: Default
    probability = 0.65
    
    explanation = explainer.generate_explanation(prediction, probability, sample_customer_features, sample_shap_values)
    print("\nLLM Explanation:")
    print(json.dumps(explanation, indent=2))
    
    copilot_question = "Why was this loan rejected?"
    copilot_answer = explainer.risk_analyst_copilot(copilot_question, explanation)
    print(f"\nCopilot Answer to \"{copilot_question}\":")
    print(copilot_answer)
