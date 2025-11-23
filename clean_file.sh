#!/bin/bash

# Kontrollera om en fil sökväg har angetts
if [ -z "$1" ]; then
  echo "Användning: $0 <fil_sökväg>"
  exit 1
fi

FILE_PATH="$1"

# Kontrollera om filen existerar
if [ ! -f "$FILE_PATH" ]; then
  echo "Fel: Filen '$FILE_PATH' hittades inte."
  exit 1
fi

# De rader som ska tas bort (använd \ för att escapa punkter i regex)
PATTERNS=(
  "system_name_Tool = Tool"
  "system_name_G5x = G5x"
  "system_name_Rot = Rot"
  "system_name_G92 = G92"
  "system_name_G54 = G54"
  "system_name_G55 = G55"
  "system_name_G56 = G56"
  "system_name_G57 = G57"
  "system_name_G58 = G58"
  "system_name_G59 = G59"
  "system_name_G59\.1 = G59\.1"
  "system_name_G59\.2 = G59\.2"
  "system_name_G59\.3 = G59\.3"
)

# Skapa en sed-expression för att ta bort raderna
SED_EXPRESSION=""
for PATTERN in "${PATTERNS[@]}"; do
  SED_EXPRESSION+="/^${PATTERN//\//\\/}\$/d;" # Escape slashes in pattern
done

# Ta bort raderna från filen
# Använder -i för att redigera filen på plats. Skapa gärna en backup först!
sed -i "$SED_EXPRESSION" "$FILE_PATH"

if [ $? -eq 0 ]; then
  echo "De angivna raderna har tagits bort från '$FILE_PATH'."
else
  echo "Ett fel uppstod när raderna skulle tas bort från '$FILE_PATH'."
fi
