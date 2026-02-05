#!/usr/bin/env python3
"""
Download Aya 23 model from HuggingFace Hub
"""

import argparse
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def parse_args():
    parser = argparse.ArgumentParser(description="Download Aya 23 model")
    parser.add_argument(
        "--model",
        type=str,
        default="CohereForAI/aya-23-8B",
        help="Model identifier on HuggingFace Hub"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./models/base/aya-23-8b",
        help="Output directory for downloaded model"
    )
    parser.add_argument(
        "--quantization",
        type=str,
        choices=["none", "int8", "int4"],
        default="none",
        help="Quantization level (reduces model size and VRAM usage)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    print("🚀 Downloading Aya 23 Model")
    print(f"Model: {args.model}")
    print(f"Output: {args.output}")
    print(f"Quantization: {args.quantization}")
    print()
    
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Download tokenizer
    print("📖 Downloading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    tokenizer.save_pretrained(str(output_path))
    print("✅ Tokenizer downloaded")
    
    # Download model with optional quantization
    print("\n🤖 Downloading model...")
    if args.quantization == "int8":
        print("  Using INT8 quantization (reduces VRAM by ~50%)")
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            load_in_8bit=True,
            device_map="auto",
            trust_remote_code=True
        )
    elif args.quantization == "int4":
        print("  Using INT4 quantization (reduces VRAM by ~75%)")
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            load_in_4bit=True,
            device_map="auto",
            trust_remote_code=True
        )
    else:
        print("  Using full precision (FP16)")
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
    
    # Save model
    model.save_pretrained(str(output_path))
    print("✅ Model downloaded")
    
    # Print info
    print(f"\n📊 Model Information:")
    print(f"  Parameters: ~8 billion")
    print(f"  Location: {output_path}")
    print(f"  Size on disk: {sum(f.stat().st_size for f in output_path.rglob('*') if f.is_file()) / (1024**3):.2f} GB")
    
    print("\n✅ Download complete!")
    print("\nNext steps:")
    print(f"  1. Set MODEL_PATH={output_path} in your .env file")
    print(f"  2. Run: python scripts/run_server.py")

if __name__ == "__main__":
    main()
