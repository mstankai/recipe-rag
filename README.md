# Guardian Recipe Chatbot

A RAG-based chatbot for interactions with Guardian Recipes.

## Table of Contents

- [About](#about)
- [Setup](#setup)
- [Usage](#usage)

## About

This project is a chatbot that uses the RAG (Retrieval-Augmented Generation) model to interact with Guardian Recipes.

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/mstankai/recipe-rag.git
    cd recipe-rag
    ```

1. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

1. **Install dependencies :**
    ```sh
    pip install -r requirements.txt
    pip install -e .

    ```

1. **Set up your Guardian API key:**
    You can set up an API key on the Guardian Open Platform page, here: [Guardian Open Platform | Getting Started](https://open-platform.theguardian.com/access/).

    Store your API key in your system's keychain using the following command:
    ```sh
    python -c 'import keyring; keyring.set_password("system", "guardian_api_key", "<your-api-key>")'
    ```sh
    You will need this to download the Guardian Recipes.


## Usage

TBA
```sh
...
```

