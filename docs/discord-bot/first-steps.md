## Que es lo que un usuario hace en discord? Que tanto tiempo esta ahi haciendo dios sepa que cosas?

- Pues esa es la gran cuestion, en este documento veremos que informacion podemos extraer de los usuarios (de manera legal claro esta)

### Objetivo
- Registrar la actividad de los usuarios de un servidor de Discord para:
- - Analizar tiempo de conexión, presencia, y participación.

- - Simular un flujo de extracción → envío (RabbitMQ) → procesamiento (API) → almacenamiento (Data Warehouse).

### Datos que podemos obtener (de forma legal y dentro de las limitaciones de Discord.py)


| Tipo de evento           | Evento de Discord.py                    | Qué podemos registrar                                    | Ejemplo de uso                                      |
| ------------------------ | --------------------------------------- | -------------------------------------------------------- | --------------------------------------------------- |
| **Conexión/desconexión** | `on_member_join`, `on_member_remove`    | Cuándo entra o sale del servidor.                        | Saber cuántos usuarios se unen o se van por semana. |
| **Cambio de estado**     | `on_presence_update`                    | Si un usuario está “online”, “idle”, “dnd”, “offline”.   | Calcular tiempo promedio en línea.                  |
| **Actividad de voz**     | `on_voice_state_update`                 | Si entra/sale de un canal de voz, mutea/desmutea, etc.   | Medir tiempo en canales de voz.                     |
| **Mensajes enviados**    | `on_message`                            | Cuándo y cuántos mensajes envía.                         | Contar mensajes por usuario/semana.                 |
| **Reacciones**           | `on_reaction_add`, `on_reaction_remove` | Qué mensajes reaccionan, y con qué emoji.                | Analizar participación emocional.                   |
| **Roles y permisos**     | A través de `member.roles`              | Roles asignados (por ejemplo, moderador, miembro nuevo). | Segmentar actividad por rol.                        |
