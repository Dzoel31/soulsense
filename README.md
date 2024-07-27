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
2. Create python virtual environment

    ```bash
    python -m venv venv
    ```

    ```bash
    source venv/bin/activate
    ```

    or

    ```bash
    venv\Scripts\activate
    ```

    on Windows

3. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Setup environment variables (copy the `.env.example` file to `.env` and fill in the values)

    for `IP4_ADDRESS`, you can run

    ```bash
    ipconfig
    ```

    to get the IP address of the machine
5. For `USER` and `PASSWORD`, you should have a MongoDB account. You can create one [here](https://www.mongodb.com),create a cluster and get the connection string.
6. Run the Flask server
7. Run the Streamlit app
8. Go to http://localhost:8501 to view the web app