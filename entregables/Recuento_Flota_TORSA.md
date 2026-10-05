# Recuento de flota TORSA — vehículos, sistemas y horas

Corte: 04/10/2026 · Supuesto de operación: 20 h/día desde el primer día del mes de implementación.
Fuentes: Flota de TorsaCore (sitios cloud) + servidores on‑premise (Antamina, Hudbay, Marcobre, ISA de EPSA).

## Resumen general

### Por sistema

| Sistema | Unidades desplegadas | Horas acumuladas (20 h/día) |
|---|---:|---:|
| CMS (anticolisión) | 462 | 6.784.500 |
| WBVM (Whole Body Vibration Monitor) | 185 | 9.173.400 |
| FAS (fatiga) | 86 | 782.000 |
| ISA (intervención) | 38 | 118.560 |
| **Total sistemas** | **771** | **16.858.460** |

### Por vehículo

| Indicador | Valor |
|---|---:|
| Vehículos instalados | 647 |
| Vehículos en sitios cloud (Flota) | 426 |
| Vehículos en servidores on‑premise | 221 |
| Horas‑vehículo acumuladas (20 h/día) | 15.967.100 |
| Sitios productivos | 14 (11 cloud + 3 on‑premise) |
| Vehículos en línea ahora (solo cloud) | 247 |

## Detalle por sitio

| Sitio | Servidor | Vehículos | Sistemas | Implementación | Días | Horas‑vehículo |
|---|---|---:|---|---|---:|---:|
| Antamina | On‑premise | 150 | WBVM 150 | 11/2018 (versión nueva desde 06/2024) | 2.894 | 8.682.000 |
| Antapaccay | Cloud | 195 | CMS 195 | 01/2023 | 1.372 | 5.350.800 |
| EPSA Alkhabra | Cloud + ISA on‑premise | 102 | CMS 101 · FAS 85 · ISA 38 | 07/2025 (ISA 05/2026) | 460 | 938.400 |
| Hudbay | On‑premise | 35 | WBVM 35 | 11/2024 | 702 | 491.400 |
| Elandsfontein | Cloud | 40 | CMS 40 | 02/2026 | 245 | 196.000 |
| Koedoeskloof | Cloud | 23 | CMS 23 | 01/2026 | 276 | 126.960 |
| Sedibeng | Cloud | 43 | CMS 43 | 06/2026 | 125 | 107.500 |
| Drummond | Cloud | 3 | CMS 3 | 08/2024 | 794 | 47.640 |
| EPSA Commodore | Cloud | 12 | CMS 12 | 08/2026 | 64 | 15.360 |
| MEL | Cloud | 6 | CMS 6 | 08/2026 (~2 meses) | 61 | 7.320 |
| Altonorte | Cloud | 1 | CMS 1 | 04/2026 | 186 | 3.720 |
| Marcobre | On‑premise | 36 | CMS 36 | sin fecha | – | pendiente |
| KARO | Cloud | 1 | CMS 1 | en instalación | 0 | 0 |
| **Total** | | **647** | **771** | | | **15.967.100** |

Marcobre: 29 camiones + 4 tractores de rueda + 3 palas.

### Horas por sistema y sitio

| Sitio | CMS | FAS | ISA | WBVM |
|---|---:|---:|---:|---:|
| Antapaccay | 5.350.800 | – | – | – |
| EPSA Alkhabra | 929.200 | 782.000 | 118.560 | – |
| Sedibeng | 107.500 | – | – | – |
| Elandsfontein | 196.000 | – | – | – |
| Koedoeskloof | 126.960 | – | – | – |
| EPSA Commodore | 15.360 | – | – | – |
| MEL | 7.320 | – | – | – |
| Drummond | 47.640 | – | – | – |
| Altonorte | 3.720 | – | – | – |
| KARO | 0 | – | – | – |
| Antamina | – | – | – | 8.682.000 |
| Hudbay | – | – | – | 491.400 |
| Marcobre | pendiente | – | – | – |
| **Total** | **6.784.500** | **782.000** | **118.560** | **9.173.400** |

## Supuestos y notas

- Antamina cuenta desde 11/2018 (primera instalación); la versión nueva del WBVM opera desde 06/2024.
- Las horas se calculan como vehículos × días desde el día 1 del mes de implementación × 20 h/día. Con 24 h/día multiplicar por 1,2.
- Los 38 camiones con ISA en EPSA forman parte de los 102 vehículos de Alkhabra; ISA se cuenta desde 05/2026.
- El FAS de Alkhabra se asume instalado junto con el CMS (07/2025).
- Los totales de Flota (426 CMS, 86 FAS en cloud) incluyen 1 CMS y 1 FAS que las capturas no permiten atribuir a un sitio; se suman al total pero sin horas.
- Hudbay figura en Flota como sitio sin respuesta; se cuentan solo los 35 camiones WBVM on‑premise.
- Marcobre no figura en Flota; va completo como on‑premise y sus horas quedan pendientes de la fecha de implementación.
- KARO está en instalación: cuenta como vehículo y sistema, con 0 horas.
