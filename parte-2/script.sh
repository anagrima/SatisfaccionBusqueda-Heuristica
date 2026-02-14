#!/usr/bin/env bash
set -uo pipefail

# Intérprete y script; puedes sobreescribir con variables de entorno
PYTHON="${PYTHON:-python}"
SCRIPT="parte-2.py"

# Siempre ejecutamos desde la carpeta del script para que encuentre los .gr/.co
cd "$(dirname "$0")"

CASES=(
    "1;5;prueba-1;salida1"
    "1;6;prueba-2;salida2"
    "1;1;prueba-3;salida3"
    "1;30;prueba-4;salida4"
    "1;7;prueba-1;salida5"
    "1;4;prueba-6;salida6"
    "1;309;USA-road-d.BAY;salida7"
)

echo "== Ejecutando pruebas =="
status=0

for row in "${CASES[@]}"; do
    IFS=';' read -r origen destino mapa salida <<< "$row"

    echo
    echo "--------------------------------------------"
    echo "Ejecutando: $origen -> $destino (mapa=$mapa)"
    echo "--------------------------------------------"

        if ! "$PYTHON" "$SCRIPT" "$origen" "$destino" "$mapa" "$salida"; then
                echo "FALLO en $origen -> $destino (mapa=$mapa)" >&2
                status=1
        fi
done

echo
if [ "$status" -eq 0 ]; then
    echo "OK: pruebas finalizadas."
else
    echo "Pruebas finalizadas con fallos." >&2
fi
exit "$status"