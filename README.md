

## Cheatsheet

```bash
conda env export | grep -v "^prefix: " > aerodev.yml
```

```bash
conda env create -f aerodev.yml
```

```bash
pip install typer
pip install -U black
pip install gpiozero pigpio

```