def generate_report(text, a):
    report = f"""
NarrativeNexus Report
---------------------

Word Count: {a.get('word_count')}
Sentence Count: {a.get('sentence_count')}

Overall Sentiment: {a.get('overall_sentiment')}

Top Keywords:
{', '.join(a.get('top_keywords', []))}

LDA Topics:
{', '.join(a.get('topics', {}).get('lda', []))}

NMF Topics:
{', '.join(a.get('topics', {}).get('nmf', []))}

Summary:
{a.get('summary')}

Insights:
"""
    for i in a.get("insights", []):
        report += f"- {i}\n"

    return report
