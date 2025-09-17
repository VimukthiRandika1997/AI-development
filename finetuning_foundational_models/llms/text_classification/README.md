# Fine-Tuning LLM for Text Classification

In this project, `Phi-3.5-min-instruct` model is finetuned for Spam Classification task.

This is adapted and restructured from the blog post: [link](https://www.datacamp.com/tutorial/fine-tuning-phi-3-5)

- There're two classes: `spam` or `not_spam`

The model is evaluated in two ways:

1. Evaluate with the base-model (using only pre-trained weights)
2. Evaluate with a finetuned version (using LoRa layers)

## Project Structure

```markdown
text_classification/
├── data
├── src/
│   ├── notebooks
        ├── exp.ipynb
│   ├── config.py
│   └── dataset.py
│   └── evaluate.py
│   └── inference.py
│   └── inference.py
│   └── metrics.py
│   └── train.py
│   └── upload_model.py
├── scripts
│   └── train_job.py
└── requirements.txt
```


## How to run:

1. Create a `.env` file in `src/.env` 

    ```bash
    # Then add your HF token and Weight and Biases token
    cp .env.sample .env
    ```

2. Create virtual environment

    ```bash
    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt
    ```

3. Start training job

    ```bash
    bash scripts/train.sh
    ```

4. Evaluate the model performance

    ```bash
    bash scripts/eval_job.sh
    ```