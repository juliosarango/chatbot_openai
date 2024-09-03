import os
import pandas as pd
import matplotlib.pyplot as plt
import base64

from openai import OpenAI
from dotenv import load_dotenv
    
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")        
)

datos = client.fine_tuning.jobs.retrieve(os.environ.get("OPENAI_ID_MODELO"))

# Obtener el archivo de resultados
content = client.files.content('file-X7NSSNJ3V9pzVMWTLtvFfmqZ')

with open("result.csv", "wb") as f:
   f.write(base64.b64decode(content.text.encode("utf-8")))


df = pd.read_csv('result.csv')
df = df.apply(pd.to_numeric, errors='coerce')
df.tail()


#conversión a numéricos para graficación
df = df.apply(pd.to_numeric, errors='coerce')
df.tail()

# Gráfica de ganancia
plt.figure(figsize=(7,4))
plt.plot(df['step'], df['train_accuracy'])
plt.title('Training Accuracy over Steps')
plt.xlabel('Step')
plt.ylabel('Training Accuracy')
plt.show()


# Gráfica de pérdida
plt.figure(figsize=(7,4))
plt.plot(df['step'], df['train_loss'])
plt.title('Training Loss over Steps')
plt.xlabel('Step')
plt.ylabel('Training Accuracy')
plt.show()



