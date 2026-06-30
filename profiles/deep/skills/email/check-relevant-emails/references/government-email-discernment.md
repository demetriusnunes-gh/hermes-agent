# Distinguishing Real Government Emails from News/Media Coverage

## Problem
The skill flags emails containing government keywords (like "governo", "multa", "IPTU", etc.) but needs to distinguish between:
1. Actual government communications requiring action
2. News/media/newsletter content merely discussing government topics

## False Positive Examples from Experience
- Newsletters from media outlets (e.g., G1 <g1@newsletterg1.globo.com>) with subjects like "Governo publica regras do novo Desenrola..."
- Blog posts or news articles mentioning government policies
- Newsletter promotional content using government keywords for clickbait

## Discernment Guidelines
When evaluating government keyword matches in email subjects:

### 1. Check Sender Identity
**Likely REAL government email if sender:**
- Ends with `.gov.br` (federal, state, or municipal government)
- Contains official government domains (e.g., `planalto.gov.br`, `receita.fazenda.gov.br`)
- Contains obvious government agency names in domain or sender name

**Likely NEWSLETTER/MEDIA if sender:**
- Contains words like: "newsletter", "news", "blog", "midia", "jornal", "revista", "portal"
- Comes from known media domains (g1.globo.com, folha.uol.com.br, estatadao.com.br, etc.)
- Is a commercial/promotional sender using government topics

### 2. Evaluate Context Beyond Keywords
**More likely REAL government action required if email:**
- Contains specific calls to action (pay taxes, respond to summons, update registration)
- References specific personal data (tax ID, license number, address)
- Comes from a specific government agency relevant to recipient's situation
- Includes official document numbers or protocols

**More likely NEWSLETTER if email:**
- Discusses government topics in general/news format
- Lacks personalization or specific action items
- Contains promotional/marketing language
- Is part of a regular newsletter distribution

### 3. Special Handling for Ambiguous Keywords
Particularly for "ir" (which can mean "to go" in Portuguese):
- Require additional verification beyond just the keyword match
- Look for context indicating tax-related meaning (Imposto de Renda)
- Check for accompanying financial/document-related language

## Implementation Approach
When a government keyword match is found:
1. First check if sender domain is `.gov.br` → if yes, flag as relevant
2. If not, evaluate sender for newsletter/media indicators
3. If sender appears to be newsletter/media, apply additional scrutiny:
   - Require multiple government keywords OR
   - Look for specific action-oriented language OR
   - Check for personal data references
4. Only flag as relevant if passes additional scrutiny

## Examples
**FLAG as relevant:**
- From: `noreply@recepcao.fazenda.gov.br` | Subject: `Notificação de lançamento do IPTU 2026`
- From: `atendimento@detran.rj.gov.br` | Subject: `Intimação para apresentação de documentação`

**DO NOT flag (newsletter/media):**
- From: `g1@newsletterg1.globo.com` | Subject: `Governo publica regras do novo Desenrola...`
- From: `newsletter@exemplo.com.br` | Subject: `Entenda as novas regras do governo sobre...`

This approach reduces false positives while maintaining capture of actual government communications requiring user attention.
