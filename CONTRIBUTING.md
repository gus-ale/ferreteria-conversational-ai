# Contribuir

## Preparación

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
```

## Antes de enviar cambios

```bash
ruff check .
ruff format --check .
pytest --cov=app
python -m evals.run_evals
```

No incluya:

- `.env`;
- API keys;
- transcripciones reales;
- información personal;
- contraseñas de bases de datos;
- datos comerciales sin autorización.

Los cambios de prompts, herramientas o intenciones deben incorporar una prueba
o un caso de evaluación que describa el comportamiento esperado.

