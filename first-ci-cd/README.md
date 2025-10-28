# Que es CI/CD?
* CI/CD es un conjunto de prácticas y herramientas automáticas que ayudan a los equipos a entregar software de manera más rápida y fiable.
| Práctica | ¿Qué hace? | ¿Para qué sirve? |
|---|---|---|
| **CI (Integración Continua)** | Automatiza la construcción y prueba del código cada vez que hay un cambio. | 🧪 Encontrar bugs y errores de integración rápidamente. |
| **CD (Entrega/Despliegue Continuo)** | Automatiza la liberación y despliegue del código que ya pasó las pruebas. | 🚀 Entregar valor a los usuarios de forma rápida y segura. |

---

#Que es GitHub Actions?

**GitHub Actions** es una plataforma de automatización integrada directamente en tu repositorio de GitHub.

En pocas palabras, te permite **automatizar tus flujos de trabajo** de software. Es como tener un robot que puede construir, probar y desplegar tu código por ti, sin que tengas que hacerlo manualmente.

### ¿Qué me permite hacer?

GitHub Actions usa "workflows" (flujos de trabajo) que tú mismo defines. Estos flujos se pueden activar automáticamente por eventos de GitHub, como:

* Hacer un `push` a una rama.
* Crear un *Pull Request*.
* Publicar un *Release*.
* O incluso a una hora programada (ej. todos los lunes a las 9:00 AM).

### ¿Para qué se usa principalmente?

Su uso más común es para **CI/CD (Integración Continua y Despliegue Continuo)**.

Esto significa que puedes configurar un *workflow* para que, cada vez que subes código nuevo:

1.  **Construya** tu proyecto (Compile el código).
2.  **Pruebe** el código (Ejecute tests automáticos para encontrar bugs).
3.  **Despliegue** tu aplicación (La publique en un servidor o una web).

Es la herramienta que conecta tu código (`git push`) con el mundo real (tu aplicación funcionando).

## Conceptos de uso de workflows:

| Conceptos | Qué significa |
|---|---|
| Workflow | Un flujo de tareas automatizadas |
| Job | Un grupo de pasos que se ejecutan |
| Step | Una acción específica (comando o tarea) |
| Runner | Máquina que ejecuta los jobs |

---

# Primer Workflow CI/CD

## 1.Crear tu proyecto
```bash
git clone https://github.com/TU_USUARIO/first-ci-cd.git
cd first-ci-cd
```

## 2.Crear la estructura
```bash
mkdir -p .github/workflows
nano .github/workflows/hola-mundo.yml
```

## 3.Crear el workflow hola-mundo.yml
```yml
name: Mi Primer CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  saludar:
    runs-on: ubuntu-latest
    steps:
    - name: 📥 Descargar código
      uses: actions/checkout@v4

    - name: 👋 ¡Hola mundo DevOps!
      run: |
        echo "¡Hola DevOps con Roxs! 🚀"
        date
        uname -a

    - name: 🧪 Test Matemático
      run: |
        if [ $((2+2)) -eq 4 ]; then
          echo "✅ Todo OK"
        else
          echo "❌ Algo falló"
          exit 1
        fi
```
## 4.Subir repo con los cambios 
```bash
git add .
git commit -m "My first action"
git push -u origin main
```

---

# Ejercicios practicos

## Ejercicio 1: Workflow con variables
name: Variables DevOps

on: [push, workflow_dispatch]

env:
  PROYECTO: "Mi App DevOps"
  AMBIENTE: "Desarrollo"

jobs:
  mostrar:
    runs-on: ubuntu-latest
    env:
      RESPONSABLE: "Estudiante DevOps"
    steps:
    - name: Mostrar info
      run: |
        echo "Proyecto: $PROYECTO"
        echo "Ambiente: $AMBIENTE"
        echo "Responsable: $RESPONSABLE"

## Ejercicio 2: Workflow condicional
name: Rama Detectada

on:
  push:
    branches: [main, develop, feature/*]
  workflow_dispatch:

jobs:
  detectar:
    runs-on: ubuntu-latest
    steps:
    - name: Detectar rama
      run: |
        echo "Rama actual: ${{ github.ref_name }}"

---

#Desafio diario

## Crea tu primer workflow basico
``` yml
name: first-basic-workflow

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  calculadora:
    runs-on: ubuntu-latest
    steps:
    - name: Sumar
      run: |
        echo "2 + 2 = 4" 
    - name: Restar
      run: |
        echo "2 - 2 = 0"
    - name: Multiplicar
      run: |
        echo "2 * 2 = 4"
    - name: Dividir
      run: |
        echo "2 / 2 = 1"
```

## Crea uno con variables
```yml
name: desafio1-b-variables

on: [push]

env:
  NUM_A: "3"
  NUM_B: "2"

jobs:
  calculadora_2_0:
    runs-on: ubuntu-latest
    steps:
    - name: Sumar
      run: |
        RESULTADO=$((NUM_A + NUM_B))
        echo "El resultado de $NUM_A + $NUM_B es: $RESULTADO"
    - name: Restar
      run: |
        RESULTADO=$((NUM_A - NUM_B))
        echo "El resultado de $NUM_A - $NUM_B es: $RESULTADO"
    - name: Multiplicar
      run: |
        RESULTADO=$((NUM_A * NUM_B))
        echo "El resultado de $NUM_A * $NUM_B es: $RESULTADO"
    - name: Dividir
      run: |
        RESULTADO=$((NUM_A / NUM_B))
        echo "El resultado de $NUM_A / $NUM_B es: $RESULTADO"
```

## Crea uno con condicionales segun la rama
```yml
name: desafio1-b-variables

on:
  push:
    branches: [main, develop]
  workflow_dispatch:

env:
  NUM_A: "3"
  NUM_B: "2"

jobs:
  detectar:
    runs-on: ubuntu-latest
    steps:
    - name: Detectar rama
      run: |
        echo "Rama actual: ${{ github.ref_name }}"

  Sumar_main:
    if: ${{ github.ref_name == 'main' }}
    needs: detectar
    runs-on: ubuntu-latest
    steps:
    - name: Sumar
      run: |
        RESULTADO=$((NUM_A + NUM_B))
        echo "El resultado de $NUM_A + $NUM_B es: $RESULTADO"

  Restar_develop:
    if: ${{ github.ref_name == 'develop' }}
    needs: detectar
    runs-on: ubuntu-latest
    steps:
    - name: Restar
      run: |
        RESULTADO=$((NUM_A - NUM_B))
        echo "El resultado de $NUM_A - $NUM_B es: $RESULTADO"
```

