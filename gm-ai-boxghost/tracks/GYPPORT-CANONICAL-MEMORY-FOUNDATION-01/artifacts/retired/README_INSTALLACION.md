# Instalación — archivos de agentes GYPPORT

Copiar estos archivos al lugar donde mantienes las instrucciones de agentes de GYPPORT.

Recomendación:

```text
GYPPORT/
├── Gystigo/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── CHATGPT.md
│   └── CODEX.md
├── Fabric/
│   └── Knowledge/
│       └── 00-GYPPORT-UNIVERSE/
│           └── GYPPORT_UNIVERSE_CANONICAL_BASELINE.md
└── Modules/
```

Si ya existen AGENTS.md, CLAUDE.md o CHATGPT.md con reglas específicas que todavía son válidas,
no sobrescribir a ciegas: comparar y conservar las reglas vigentes que no contradigan el nuevo baseline.

La pieza estable es el Mandatory Knowledge Gate; los detalles arquitectónicos deben vivir en Fabric/Knowledge.
