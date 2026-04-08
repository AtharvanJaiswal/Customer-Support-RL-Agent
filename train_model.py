from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer
import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# -----------------------------
# LOAD DATASET
# -----------------------------
dataset = load_dataset("json", data_files="clean_dataset.json")

# -----------------------------
# FORMAT DATA
# -----------------------------
def format_example(example):
    return {
        "text": f"""
        ### Instruction:
        You are a professional customer support agent. Always respond politely and helpfully.

        ### Input:
        User Query: {example['query']}

        ### Output:
        Category: {example['category']}
        Priority: {example['priority']}
        Response: {example['response']}
        """
    }

dataset = dataset.map(format_example)

# -----------------------------
# LOAD MODEL
# -----------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.to(device)

# fix padding
tokenizer.pad_token = tokenizer.eos_token

# -----------------------------
# TRAINING CONFIG
# -----------------------------
training_args = TrainingArguments(
    output_dir="./model",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    logging_steps=1,
    save_strategy="no",
    fp16=True,
    dataloader_pin_memory=True,
    no_cuda=False
)

# -----------------------------
# TRAINER
# -----------------------------
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    processing_class=tokenizer,   # ✅ FIX
    args=training_args,
)
# -----------------------------
# TRAIN
# -----------------------------
trainer.train()

# -----------------------------
# SAVE MODEL
# -----------------------------
trainer.save_model("support_model")

print("✅ Model trained and saved!")