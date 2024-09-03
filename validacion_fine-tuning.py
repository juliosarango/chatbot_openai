import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model=os.environ.get("OPENAI_MODEL_FINE_TUNING"),
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Eres un asistente de atención a clientes y estudiantes de la plataforma de educación online en tecnología, inglés y liderazgo llamada Platzi",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Que cursos tomar para aprender blockchain?"}
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Que cursos tomar para aprender blockchain?"}
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Para aprender sobre blockchain, te recomendamos tomar la Ruta de Blockchain en Platzi. Esta ruta incluye cursos que te enseñarán desde los fundamentos de blockchain hasta su aplicación en diferentes industrias. ¡Aprende con los mejores expertos en Platzi y conviértete en un experto en blockchain!",
                }
            ],
        },
    ],
    temperature=0.02,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={"type": "text"},
)

print(response.choices[0].message.content)
