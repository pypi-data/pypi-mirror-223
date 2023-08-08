# **MLE-Training**

## **Project Description**

Predicting median house value on given housing data.

## Command to create mle-dev environment

```bash
conda env create -f env.yml
```

## Command to activate the environment

```bash
conda activate mle-dev
```

## Command to run python script

```bash
python nonstandardcode.py
```

---

## **Manual Refactoring of Python Code**

## Command to refactor python code using isort

```bash
isort nonstandardcode.py
```

```bash
isort --profile black nonstandardcode/nonstandardcode.py
```

## Command to refactor python code using black

```bash
black nonstandardcode.py
```

## Command to refactor entire python project using black

```bash
black --config pyproject.toml .
```

## Command to refactor python code using flake8

```bash
flake8 nonstandardcode.py
```

## Command to refactor entire python project using flake8

```bash
flake8 --config setup.cfg .
```
