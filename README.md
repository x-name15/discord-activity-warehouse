# Discord Activity Warehouse

## Descripción
Este proyecto captura **eventos de actividad de usuarios en un servidor de Discord** y los envía a un sistema de mensajería (RabbitMQ) para su posterior almacenamiento y análisis en un microservicio/Data Warehouse.

---

## Componentes

| Componente | Tecnología | Función |
|-----------|------------|--------|
| Bot de Discord | discord.py | Escucha eventos de usuarios en tiempo real: unirse/salir, presencia, mensajes, voz, reacciones, roles. |
| Mensajería | RabbitMQ | Cola para enviar eventos del bot al microservicio de forma desacoplada. |
| Microservicio | Express + TypeScript | Consumirá los eventos de RabbitMQ y los almacenará en PostgreSQL. |
| Data Warehouse | PostgreSQL | Base de datos relacional para análisis histórico y dashboards. |
| Dashboard | Streamlit / Metabase | Visualización de métricas y actividad de usuarios. |
| Orquestación | Docker + docker-compose | Levanta todos los servicios de manera reproducible. |

---

## Cómo funciona

1. El **bot** detecta cambios en Discord (presencia, voz, mensajes, reacciones, roles, miembros).  
2. Cada evento se convierte a JSON y se envía a **RabbitMQ**.  
3. El **microservicio** consume estos eventos y los guarda en la base de datos.  
4. Desde la base de datos se pueden generar **dashboards y métricas**, como tiempo total online, actividad por canal, mensajes enviados, roles activos, etc.

---

## Beneficios educativos

- Introducción a **bots de Discord** y eventos de presencia/actividad.  
- Uso de **colas de mensajería (RabbitMQ)** y microservicios.  
- Integración con **base de datos relacional para analítica**.  
- Visualización y dashboards interactivos.  
- Preparación para un **portafolio open-source** para primer año de informática.

---

## Próximos pasos

- Crear el **microservicio en TypeScript + Express**.  
- Consumir eventos de RabbitMQ y almacenarlos en PostgreSQL.  
- Generar **dashboards** de presencia y actividad.



