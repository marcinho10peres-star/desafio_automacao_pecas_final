# Documento Teórico — Desafio Automação Digital

## 1. Contextualização
A automação da inspeção de peças reduz falhas humanas, aumenta a velocidade de inspeção e fornece rastreabilidade do processo produtivo. Este protótipo demonstra como regras de qualidade podem ser aplicadas de forma automatizada, com armazenamento físico das peças aprovadas (simulado por caixas).

## 2. Estrutura da solução
A solução foi organizada em três classes principais:
- `Part`: representa uma peça, contém dados e métodos de avaliação.
- `Box`: representa uma caixa física de armazenamento, mantém IDs das peças e estado (fechada/aberta).
- `Warehouse`: coordena partes, caixas e persistência (carregamento/salvamento em JSON).

Fluxo ao cadastrar:
1. Usuário insere medidas (peso, cor, comprimento).
2. O sistema cria um objeto `Part` e chama `evaluate()`.
3. Se aprovado, a peça é inserida na caixa aberta atual; caso contrário, registra motivos.
4. Estado salvo em `data_store.json`.

## 3. Decisões de implementação
- **JSON para persistência**: formato simples e legível, suficiente para protótipo.
- **Caixa fechada ao atingir capacidade**: evita reuso automático e simula logística de empacotamento.
- **Não reabrir caixas automaticamente**: comportamento deliberado para simular lote fechado.
- **Export CSV**: facilita análise externa (Excel/Sheets) e entrega de relatório.

## 4. Benefícios percebidos
- Redução de tempo de inspeção manual.
- Registro de motivos de reprovação para ações corretivas.
- Facilidade para integração futura com sensores/IoT.

## 5. Desafios e limitações
- Entrada manual: em produção é necessário integrar sensores.
- Resiliência: JSON local é simples, mas para produção usar banco de dados.
- Reabertura de caixas e reconciliações não estão automatizadas.

## 6. Possíveis aprimoramentos
- Integração com dispositivos industriais (PLC, sensores).
- Interface web + API REST.
- Configuração dinâmica das regras por arquivo YAML/JSON.
- Testes unitários e pipeline CI/CD.

## 7. Conclusão
O protótipo atende aos requisitos do desafio acadêmico e oferece base sólida para expansão com IoT/IA.
