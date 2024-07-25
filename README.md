# SoulSense

## Dataset

[Kaggle: Facial Recognition](https://www.kaggle.com/datasets/apollo2506/facial-recognition-dataset)

## Tech Stack

- Flask
- TensorFlow
- Keras
- Streamlit (for the web app)
- MongoDB
- Ollama (llama3 model)

## To run llama3

1. Install the ollama software from [here](https://ollama.com/download/)
2. Pull llama3 models

    ```bash
    ollama pull llama3
    ```

3. Go to how to run section

## How to run

1. Clone the repository
2. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

3. Setup environment variables (copy the `.env.example` file to `.env` and fill in the values)
4. Run the Flask server
5. Run the Streamlit app
