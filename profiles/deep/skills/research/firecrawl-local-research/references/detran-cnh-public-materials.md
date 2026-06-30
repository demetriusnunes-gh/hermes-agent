# DETRAN / CNH public materials research notes

Use this when researching or scoping a Brazilian CNH/DETRAN test-prep product.

## Public material types found

### Official curriculum / syllabus
- The core national curriculum is public in CONTRAN rules, especially Resolução CONTRAN 789/2020 (consolidated formation-of-drivers rules).
- For first CNH categories A/B, the theoretical course is 45 horas-aula:
  - Legislação de Trânsito: 18h
  - Direção defensiva: 16h
  - Primeiros socorros: 4h
  - Proteção/respeito ao meio ambiente + convívio social: 4h
  - Funcionamento do veículo: 3h
- ACC has a shorter 20h theoretical curriculum.

### Official DETRAN educational PDFs
Examples that were publicly reachable:
- DETRAN/RS Escola Pública de Trânsito, 2025 "Caderno do Estudante" PDFs:
  - Legislação de Trânsito, Primeira Habilitação (100 pages)
  - Primeiros Socorros, Primeira Habilitação (27 pages)
  - These pages state reproduction is allowed with attribution under a Creative Commons-style license.
- DETRAN/PR PDFs:
  - Direção defensiva: `https://www.detran.pr.gov.br/arquivos/File/habilitacao/apostilas/direcaodefensiva.pdf`
  - Primeiros socorros: `https://www.detran.pr.gov.br/arquivos/File/habilitacao/apostilas/primeirossocorros.pdf`
- DETRAN/PE updated 2024 PDF:
  - Direção Defensiva e Prevenção de Sinistros: `https://www.detran.pe.gov.br/images/educacao/apostila-direcao-defensiva-prevencao-sinistros-versao-detranpe2024-compactado.pdf`

### Official simulados
- DETRAN-SP exposes a public simulado service page: `https://servicos.sp.gov.br/fcarta/2E929998-4E63-41A6-92B9-9D3F37F09F01`
- The page states questions are randomly drawn from the official Detran-SP database, similar to the real exam, and supports 1ª habilitação, renovação, and ACC.
- Treat official simulator pages as UX/style references. Do not assume the full official question bank is legally/technically bulk-downloadable.

### Legal and standards sources
- CTB (Código de Trânsito Brasileiro) and CONTRAN/SENATRAN resolutions are public and can support explanations and legal references.
- Traffic signs/road markings can be reconstructed from public definitions; avoid copying copyrighted diagrams unless license allows it.

## Useful search queries
```text
site:gov.br Senatran manual formação condutores PDF legislação trânsito direção defensiva primeiros socorros meio ambiente cidadania
DETRAN simulado prova teórica CNH questões públicas
DETRAN banco questões prova teórica legislação trânsito pública PDF
site:detran.sp.gov.br simulado prova teórica CNH
SENATRAN curso formação condutores conteúdo programático primeira habilitação
Contran resolução curso formação condutores conteúdo programático prova teórica
```

## Extraction notes
- Firecrawl may fail or return empty for PDFs. Fall back to direct `requests.get()`/`curl` and extract with Python `pypdf` if available.
- Some DETRAN/RS PDF URLs may fail TLS verification in Python; retry with `verify=False` only for retrieval, and note the certificate issue.
- If `pdftotext` is unavailable, use `pypdf`. On this Ubuntu VPS, `pip install --break-system-packages pypdf` worked, but prefer a venv when `python3-venv` is available.

## Product-scoping implications
A legitimate CNH prep product can be built from public syllabus + public DETRAN educational material + generated/reviewed questions. The defensible product layer is:
- official-syllabus map
- micro-lessons
- generated practice bank tagged by module/law reference
- 30-question simulated exam mode
- traffic-sign visual drills
- adaptive review / mistake notebook
- state-specific landing pages and metadata
- WhatsApp daily practice bot

Avoid claiming access to official question banks unless explicitly sourced/licensed.
