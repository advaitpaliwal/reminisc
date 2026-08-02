

# Reminisc

Reminisc es un framework de código abierto para la memoria de LLMs, inspirado en OpenAI.

![demo](assets/demo.gif)

## Características

- Almacena la entrada del usuario como memorias para referencia futura
- Recupera memorias relevantes basadas en las consultas del usuario
- Clasifica la entrada del usuario para determinar si debe almacenarse como una memoria
- Genera respuestas contextuales utilizando las memorias recuperadas y el historial del chat
- Utiliza un LLM para la creación de memorias y la generación de respuestas
- Se integra con Supabase y pgvector para un almacenamiento y recuperación eficiente de memorias

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/yourusername/reminisc.git
cd reminisc
```

2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
   - Crea un archivo `.env` en el directorio raíz del proyecto.
   - Agrega las siguientes variables al archivo `.env`:

```
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
```

## Configuración de Supabase

1. Inicializa Supabase: Asegúrate de tener la CLI de Supabase instalada. Si no, instálala siguiendo las instrucciones [aquí](https://supabase.io/docs/guides/cli).

2. Aplica las migraciones de la base de datos: Reinicia la base de datos de Supabase y aplica las migraciones para configurar las tablas y funciones requeridas:

```bash
supabase db reset
```

Esto ejecutará los archivos SQL en el directorio `supabase/migrations`, configurando el esquema de base de datos necesario.

## Uso

Para iniciar Reminisc:

1. Ejecuta el servidor de FastAPI:

```bash
fastapi dev main.py
```

2. En una terminal separada, ejecuta la aplicación de Streamlit:

```bash
streamlit run app.py
```

Ahora puedes interactuar con el asistente ingresando tus mensajes en la aplicación de Streamlit. El asistente generará respuestas basadas en las memorias almacenadas y el contexto de la conversación actual.

## Documentación de la API

Para obtener información detallada sobre las rutas de API disponibles y su uso, consulta la [documentación](reminisc/api/README.md).

## Configuración

Puedes modificar la configuración en el archivo `reminisc/config/config.py`. Las opciones disponibles incluyen:

- `CLASSIFIER_MODEL_NAME`: El modelo de OpenAI utilizado para clasificar la entrada del usuario (predeterminado: "gpt-3.5-turbo").
- `MEMORY_CREATOR_MODEL_NAME`: El modelo de OpenAI utilizado para crear memorias a partir de la entrada del usuario (predeterminado: "gpt-3.5-turbo").

## Contribuciones

Damos la bienvenida a contribuciones para mejorar Reminisc y expandir sus capacidades. Por favor, abre un issue para sugerencias o reportes de errores, o envía un pull request para contribuciones de código.

Áreas prioritarias para contribuciones:

- Empaquetado: Convertir este framework en un paquete de Python distribuible.
- Integraciones con LLMs: Integrar modelos de lenguaje adicionales para generar respuestas.
- Soporte para bases de datos vectoriales: Expandir el soporte para varias bases de datos vectoriales para el almacenamiento y recuperación de memorias.
- Memoria controlada por el usuario: Permitir a los usuarios instruir al asistente para recordar u olvidar información y gestionar memorias.
- Consolidación y actualización de memorias: Implementar mecanismos para consolidar y actualizar memorias y mejorar la relevancia y coherencia de las respuestas.

## Citación

Si utilizas este repositorio, por favor considera citarlo con:

```
@misc{reminisc,
   author = {Advait Paliwal},
   title = {Reminisc: Memory for LLMs},
   year = {2024},
   publisher = {GitHub},
   journal = {GitHub repository},
   howpublished = {\url{https://github.com/advaitpaliwal/reminisc}},
}
```

## Licencia

Este proyecto está licenciado bajo la [Licencia Apache](LICENSE).
