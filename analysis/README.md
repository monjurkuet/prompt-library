### Analysis

Data analysis, extraction, and insight generation prompts for processing structured and unstructured information.

## Prompts

### Data Processing

Prompts for extracting, transforming, and preparing data for downstream applications.

#### Precision Document Parser for Structured Data Extraction
Extract documents into structured semantic markdown optimized for RAG and ML training datasets.

- **Complexity:** Advanced
- **Use case:** Converting PDFs, images, and documents into machine-readable format
- **Key features:**
  - Zero-hallucination extraction
  - Verbatim content preservation
  - RAG metadata optimization
  - Visual content analysis
  - Comprehensive validation framework
- **Models:** Claude 3.5+, GPT-4, Gemini 1.5 Pro
- **Estimated time:** 20-45 minutes per document

[View prompt →](data_processing/document_parser_rag_extraction.md)

---

### Data Visualization

*Coming soon: Prompts for creating charts, graphs, and visual representations of data*

---

### Statistical Analysis

*Coming soon: Prompts for statistical analysis, hypothesis testing, and data interpretation*

---

### Financial Analysis

*Coming soon: Prompts for financial data analysis, metrics calculation, and trend analysis*

---

### Business Intelligence

*Coming soon: Prompts for business metrics, KPI analysis, and reporting*

---

## Quick Start

1. **Browse by subcategory** above
2. **Select a prompt** that matches your analysis needs
3. **Review the metadata** to ensure it fits your use case
4. **Copy the prompt** and provide your data
5. **Validate output** using the included checklist

## Subcategories

| Subcategory | Purpose | Status |
|-------------|---------|--------|
| Data Processing | Extract and transform raw data | ✅ Active |
| Data Visualization | Create visual representations | 🔄 Planned |
| Statistical Analysis | Analyze patterns and relationships | 🔄 Planned |
| Financial Analysis | Analyze financial data and metrics | 🔄 Planned |
| Business Intelligence | Generate business insights and reports | 🔄 Planned |

## Common Use Cases

### Extract Data from Documents
Use the **Precision Document Parser** to:
- Convert PDFs to structured markdown
- Extract tables and charts from reports
- Prepare documents for RAG systems
- Create ML training datasets
- Preserve source accuracy with zero hallucination

### Analyze Structured Data
*Prompts coming soon for:*
- Statistical analysis and hypothesis testing
- Trend identification and forecasting
- Correlation and regression analysis
- Anomaly detection

### Create Data Visualizations
*Prompts coming soon for:*
- Chart and graph generation
- Dashboard creation
- Visual storytelling
- Data presentation

### Financial Analysis
*Prompts coming soon for:*
- Financial metric calculations
- Portfolio analysis
- Market trend analysis
- Risk assessment

## Best Practices

### Data Quality
- Ensure source data is accurate and complete
- Validate extracted data against source
- Use validation checklists provided in each prompt
- Flag ambiguities rather than making assumptions

### RAG Optimization
- Use chunk tags strategically for retrieval
- Include metadata for filtering and searching
- Preserve document structure for context
- Test retrieval performance with sample queries

### ML Training Data
- Maintain data consistency across extractions
- Document any transformations or cleaning steps
- Include confidence ratings for uncertain data
- Preserve original formatting and errors where relevant

### Validation
- Review output against provided checklists
- Compare extracted data to source documents
- Test with sample queries or analysis
- Document any limitations or edge cases

## Integration with Other Categories

### With Trading Prompts
Use data extraction prompts to prepare market data, financial reports, and technical analysis documents for trading bot development.

### With Development Prompts
Use data processing prompts to prepare datasets for ML model training and code generation tasks.

### With Content Prompts
Use data extraction to gather information for content creation and research.

## Contributing

Have a data analysis prompt to share? See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Tags

Browse prompts by tag:
- `#data-extraction` — Document and data extraction
- `#rag` — Retrieval Augmented Generation
- `#ml-training` — Machine learning dataset preparation
- `#structured-data` — Structured data handling
- `#markdown` — Markdown formatting
- `#zero-hallucination` — Accuracy-focused prompts
- `#visualization` — Data visualization
- `#statistical-analysis` — Statistical methods
- `#financial-analysis` — Financial data analysis

## Resources

- [Prompt Index](../metadata/prompt_index.yaml) — Searchable index of all analysis prompts
- [RAG Optimization Guide](rag_optimization_guide.md) — Best practices for RAG systems
- [ML Training Data Preparation](ml_training_data_prep.md) — Guidelines for ML datasets

## FAQ

**Q: Which prompt should I use for PDF extraction?**
A: Start with the **Precision Document Parser for Structured Data Extraction**. It handles PDFs, images