# test_installation.py
import torch
import diffusers 
import datasets

print(f"PyTorch version: {torch.__version__}")
print(f"Diffusers version: {diffusers.__version__}")
print(f"Datasets version: {datasets.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"MPS (Metal Performance Shaders) available: {torch.backends.mps.is_available()}")