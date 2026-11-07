# Ctrl Free · Part 1: Run a 32B AI model for ₹0

Kaggle notebook commands (Settings → Accelerator: GPU T4 x2, Internet: on):

```
!curl -fsSL https://ollama.com/install.sh | sh
!nohup ollama serve &
!ollama pull qwen3:32b
!ollama run qwen3:32b "Explain MCP in one line"
```

- 2× T4 = 32 GB GPU memory; qwen3:32b at 4-bit is about 20 GB, so it fits across both GPUs.
- Sessions stop at 12 hours and the disk resets. Re-pull the model next time.
- Free limits change. Check your Kaggle settings.
