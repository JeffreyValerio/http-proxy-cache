# HTTP Proxy con Caché - Versión Simple

## ¿QUÉ ES UN PROXY HTTP?

**Un proxy** es como un **intermediario** entre tú (cliente) y un servidor web.

En lugar de conectarte directamente al servidor, te conectas al proxy, y **el proxy te conecta al servidor**.

```
SIN PROXY:
Cliente → Servidor

CON PROXY:
Cliente → Proxy → Servidor
```

## ¿QUÉ ES CACHÉ?

**Caché** es **memoria rápida** que guarda respuestas que ya pedimos.

```
Primera petición (CACHE MISS):
Cliente → Proxy → [Pide al servidor]
         → Guarda respuesta en caché
         → Devuelve al cliente

Segunda petición (CACHE HIT):
Cliente → Proxy → [Ya tiene en caché]
         → Devuelve rápido al cliente
         (NO pide al servidor)
```

## ¿PARA QUÉ SIRVE?

✅ **MÁS RÁPIDO:** La caché está en memoria (muy rápido)  
✅ **MENOS CARGA:** El servidor recibe menos peticiones  
✅ **MENOS ANCHO BANDA:** No se repite el tráfico de red  

**Ejemplo:**
- Sin caché: Si 100 clientes piden la misma página → 100 peticiones al servidor
- Con caché: Si 100 clientes piden la misma página → 1 petición, 99 desde caché

## ARQUITECTURA

```
CLIENTE (tu navegador)
    │
    ▼
PROXY (puerto 8888)
    │
    ├─► ¿Está en CACHÉ? ────► SÍ ──► Devuelve rápido (HIT)
    │
    └─► NO ──► Pide al BACKEND ──► Guarda en caché ──► Devuelve (MISS)
```

## TÉRMINOS CLAVE

| Término | Significado |
|---------|------------|
| **CACHE HIT** | La respuesta estaba en caché → ¡Rápido! |
| **CACHE MISS** | La respuesta NO estaba → hay que pedir al servidor |
| **TTL** | Tiempo de vida del caché (expira después) |
| **Backend** | Servidor web real |
| **Proxy** | Intermediario con caché |

## CÓMO FUNCIONA (paso a paso)

### 1. Cliente hace petición
```
Cliente: "Dame la página /inicio"
```

### 2. Proxy verifica caché
```
Proxy: "¿/inicio está en mi caché?"
```

### 3a. Si está en caché (HIT)
```
Proxy: "¡Sí! Devuelvo desde caché"
→ Cliente recibe RÁPIDO
```

### 3b. Si NO está en caché (MISS)
```
Proxy: "No está. Pido al servidor..."
→ Proxy: "Servidor me da la respuesta"
→ Proxy: "Guardo en caché"
→ Proxy: "Devuelvo al cliente"
```

## INSTALACIÓN Y USO

### Requisitos
```bash
python3.8+
docker-compose
requests (pip install requests)
```

### Ejecutar

**Opción 1: Con Docker Compose**
```bash
docker-compose up -d
```

**Opción 2: Local (solo proxy)**
```bash
pip install requests
python proxy.py
```

### Probar

```bash
# Primera petición (CACHE MISS)
curl -v http://localhost:8888/

# Segunda petición (CACHE HIT)
curl -v http://localhost:8888/

# Ver cabecera X-Cache para saber si fue HIT o MISS
# X-Cache: HIT   = vino del caché (rápido)
# X-Cache: MISS  = vino del servidor (lento)
```

## ARCHIVOS

```
.
├── proxy.py              # Proxy HTTP con caché
├── docker-compose.yml    # Stack Docker
├── app.py               # Servidor backend simple
├── requirements.txt     # Dependencias Python
└── README.md            # Este archivo
```

## VENTAJAS Y DESVENTAJAS

### ✅ VENTAJAS
- Respuestas más rápidas (desde caché)
- Menos carga en el servidor backend
- Reduce tráfico de red repetitivo
- Mejora la experiencia del usuario

### ⚠️ DESVENTAJAS
- Datos pueden estar "viejos" (expiración de caché)
- Usa memoria (caché en RAM)
- Más complejidad

## CASOS DE USO

- **Sitios web estáticos:** imágenes, CSS, JavaScript
- **APIs públicas:** respuestas que no cambian a menudo
- **Contenido educativo:** cursos, documentación
- **Streaming:** reducir carga en el servidor

## MEJORAS FUTURAS

- [ ] Invalidación manual de caché
- [ ] Diferentes TTL por tipo de contenido
- [ ] Compresión de respuestas
- [ ] Estadísticas detalladas (hits/misses %)
- [ ] Persistencia del caché (a disco)
- [ ] Límite máximo de caché en memoria

---

**Versión simplificada por:** Jeffrey Valerio  
**Basada en:** arquitectura de proxies HTTP con caché  
**Objetivo:** Entender cómo funciona un proxy con caché de forma SIMPLE
