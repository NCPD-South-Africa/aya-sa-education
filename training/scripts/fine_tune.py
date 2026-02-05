#!/usr/bin/env python3
"""
Fine-tuning script for Aya 23 on South African educational datasets
Uses LoRA (Low-Rank Adaptation) for parameter-efficient fine-tuning
"""

import os
import argparse
from pathlib import Path
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType

def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune Aya 23 for SA Education")
    parser.add_argument(
        "--model_name",
        type=str,
        default="CohereForAI/aya-23-8B",
        help="Base model to fine-tune"
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Path to training dataset (JSONL format)"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./models/fine-tuned",
        help="Directory to save fine-tuned model"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="Language for fine-tuning (en, zu, xh, af)"
    )
    parser.add_argument(
        "--num_epochs",
        type=int,
        default=3,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=4,
        help="Training batch size per device"
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=2e-4,
        help="Learning rate"
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=2048,
        help="Maximum sequence length"
    )
    return parser.parse_args()

def format_instruction(example):
    """Format instruction-response pairs for training"""
    instruction = example.get("instruction", "")
    response = example.get("response", "")
    
    # Format as instruction-following template
    text = f"### Instruction:\n{instruction}\n\n### Response:\n{response}"
    return {"text": text}

def main():
    args = parse_args()
    
    print("🚀 Starting fine-tuning for SA Edu LLM")
    print(f"Model: {args.model_name}")
    print(f"Dataset: {args.dataset_path}")
    print(f"Language: {args.language}")
    
    # Load tokenizer
    print("\n📖 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load dataset
    print("\n📚 Loading dataset...")
    dataset = load_dataset("json", data_files=args.dataset_path, split="train")
    dataset = dataset.map(format_instruction, remove_columns=dataset.column_names)
    
    # Tokenize dataset
    print("\n🔢 Tokenizing dataset...")
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=args.max_length,
            padding="max_length"
        )
    
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"]
    )
    
    # Split into train/validation
    split_dataset = tokenized_dataset.train_test_split(test_size=0.1)
    
    # Load base model
    print("\n🤖 Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Configure LoRA
    print("\n⚙️ Configuring LoRA...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,  # LoRA rank
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"],  # Adapt for Aya architecture
        bias="none"
    )
    
    # Apply LoRA to model
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.learning_rate,
        fp16=True,
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=500,
        save_total_limit=3,
        load_best_model_at_end=True,
        report_to=["tensorboard"],
        warmup_steps=100,
        optim="adamw_torch",
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=split_dataset["train"],
        eval_dataset=split_dataset["test"],
        data_collator=data_collator,
    )
    
    # Train
    print("\n🏋️ Starting training...")
    trainer.train()
    
    # Save final model
    print("\n💾 Saving model...")
    output_path = Path(args.output_dir) / f"aya-23-8b-sa-edu-{args.language}"
    trainer.save_model(str(output_path))
    tokenizer.save_pretrained(str(output_path))
    
    print(f"\n✅ Fine-tuning complete! Model saved to: {output_path}")
    print("\nNext steps:")
    print(f"  1. Evaluate model: python scripts/evaluate_model.py --model {output_path}")
    print(f"  2. Test inference: python scripts/test_inference.py --model {output_path}")
    print(f"  3. Deploy: Update MODEL_PATH in .env to {output_path}")

if __name__ == "__main__":
    main()
