from crewai import Task

def create_technical_report_task(agent, context=None):
    """Create a task for generating a technical report for Qualcomm engineers."""
    return Task(
        description=(
            "Create a comprehensive technical report detailing the 5G modem performance "
            "analysis results, identified anomalies, their root causes, and recommended "
            "optimizations. This report is intended for Qualcomm engineers with deep "
            "technical expertise in 5G modem technology.\n\n"
            "The report should be thorough and precise, including all relevant technical "
            "details, metrics, diagnostic findings, and optimization recommendations. "
            "Use appropriate technical terminology and provide detailed explanations "
            "of the analysis methodologies, findings, and reasoning behind recommendations."
        ),
        expected_output=(
            "A detailed technical report in PDF format that includes: executive summary, "
            "methodology, comprehensive performance metrics with analysis, anomaly "
            "detection results with diagnostic explanations, optimization recommendations "
            "with technical justification, and supporting data visualizations. The report "
            "should be structured for technical readers, with appropriate sections, "
            "references, and appendices for detailed data. Include specific parameter "
            "recommendations and potential firmware optimization strategies."
        ),
        agent=agent,
        context=context
    )

def create_performance_visualization_task(agent, context=None):
    """Create a task for generating performance visualizations and insights."""
    return Task(
        description=(
            "Create clear, insightful visualizations of the 5G modem performance data "
            "that highlight key metrics, trends, anomalies, and the effects of recommended "
            "optimizations. These visualizations should effectively communicate complex "
            "network performance data in an accessible, visual format.\n\n"
            "Include visualizations for key performance indicators (latency, throughput, "
            "signal strength, packet loss), anomaly detection results, before/after "
            "optimization comparisons, and correlation analyses between different metrics. "
            "Each visualization should be designed to clearly convey specific insights about "
            "the modem's performance and the impact of detected issues."
        ),
        expected_output=(
            "A set of clear, informative data visualizations with accompanying explanatory "
            "text that tells the story of the modem's performance. Each visualization should "
            "include a title, axis labels, legend, and brief analysis of what it shows. "
            "The visualizations should use appropriate chart types for different data "
            "relationships and should effectively highlight patterns, anomalies, and insights. "
            "The output should be suitable for inclusion in both technical and executive reports."
        ),
        agent=agent,
        context=context
    )

def create_executive_summary_task(agent, context=None):
    """Create a task for generating an executive summary of findings and recommendations."""
    return Task(
        description=(
            "Create a concise, high-impact executive summary that distills the key findings "
            "from the 5G modem performance analysis, highlighting the most significant "
            "insights, critical issues, and high-priority recommendations. This summary "
            "should be accessible to both technical and non-technical stakeholders.\n\n"
            "Focus on communicating the business and technical value of the analysis, "
            "emphasizing the operational impacts of the findings and the expected benefits "
            "of implementing the recommended optimizations. Prioritize clarity and "
            "actionable insights over technical detail."
        ),
        expected_output=(
            "A 1-2 page executive summary that includes: key performance findings, "
            "critical issues identified, prioritized recommendations, expected benefits "
            "of implementation, and next steps. The summary should be written in clear, "
            "concise language that communicates technical concepts effectively to both "
            "technical and business audiences. Include a few impactful visualizations "
            "or metrics that highlight the most important insights."
        ),
        agent=agent,
        context=context
    )
