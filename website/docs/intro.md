---
id: intro
title: O que é o CrewAI
sidebar_position: 1
---

# O que é o CrewAI

**CrewAI** é um framework open-source para criar **equipas de agentes de IA** que colaboram para resolver tarefas complexas.

## Elementos Principais

Cada sistema CrewAI tem três elementos fundamentais:

### 🤖 Agentes

- Especialistas numa tarefa específica
- Exemplos: investigador de notícias, analista financeiro

### 📋 Tarefas

- Definem o que precisa ser feito
- Atribuídas a agentes específicos

### 👥 Crew (Equipa)

- A equipa de agentes que executa as tarefas em conjunto

## Casos de Uso

| Caso de Uso | Descrição |
|---|---|
| 📈 Análise financeira | Análise automatizada de stocks e portfólios |
| 📄 Geração de relatórios | Relatórios profissionais em PDF/Markdown |
| 📣 Automação de marketing | Conteúdo e campanhas automáticas |
| 📰 Investigação de notícias | Recolha e síntese de informação |
| 💻 Geração de código | Criação e revisão automática de código |

## Arquitectura Conceptual

```
+-------------------+
|  Research Agent   |   ← Encontra informação
+---------+---------+
          |
          v
+-------------------+
| Technical Analyst |   ← Analisa dados
+---------+---------+
          |
          v
+-------------------+
| Investor Agent    |   ← Toma decisões
+---------+---------+
          |
          v
+-------------------+
| Writer Agent      |   ← Gera relatório
+---------+---------+
          |
          v
     PDF / Markdown
```

## Próximo passo

Continua para a [Instalação →](./installation)
