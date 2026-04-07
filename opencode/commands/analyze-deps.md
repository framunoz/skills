---
description: Analiza la arquitectura y dependencias del proyecto (Python/JS).
agent: architect
---
Analiza el siguiente mapa de dependencias del proyecto y resume la salud arquitectónica. 
Identifica dependencias circulares, acoplamiento alto o violaciones de arquitectura en capas.

Mapa de Dependencias:
!{uv run opencode/skills/system-modeler/scripts/dependency-analyzer.py $ARGUMENTS}
