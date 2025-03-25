from crewai import Task

def create_anomaly_detection_task(agent, context=None):
    """Create a task for detecting anomalies in network performance data."""
    return Task(
        description=(
            "Using the provided network performance metrics, identify any anomalies "
            "or patterns that indicate potential issues with the 5G modem's operation. "
            "Apply statistical analysis and domain knowledge to detect both obvious and "
            "subtle abnormalities in latency, throughput, signal strength, packet loss, "
            "and connection metrics.\n\n"
            "Consider correlations between different metrics that might indicate specific "
            "types of problems. Look for both single-point anomalies and problematic "
            "trends over time."
        ),
        expected_output=(
            "A comprehensive list of detected anomalies, with each anomaly clearly "
            "described and categorized by type, severity, and affected performance "
            "area. For each anomaly, include the specific metrics and values that "
            "indicate the problem, as well as a confidence assessment of the detection. "
            "The output should be structured for easy integration into diagnostic processes."
        ),
        agent=agent,
        context=context
    )

def create_diagnostic_analysis_task(agent, context=None):
    """Create a task for diagnosing the root causes of detected anomalies."""
    return Task(
        description=(
            "For each detected anomaly in the 5G modem performance data, conduct a "
            "thorough diagnostic analysis to identify potential root causes. Apply "
            "your expertise in 5G technologies and network protocols to trace each "
            "symptom to its likely underlying causes.\n\n"
            "Consider both common and rare causes for each type of anomaly, and "
            "evaluate the likelihood of each potential cause based on the specific "
            "patterns observed in the data. Look for relationships between different "
            "anomalies that might point to a common root cause."
        ),
        expected_output=(
            "A detailed diagnostic report that maps each detected anomaly to its most "
            "likely root causes, with explanations of the diagnostic reasoning and "
            "evidence supporting each conclusion. The report should prioritize causes "
            "by likelihood and provide a confidence assessment for each diagnosis. "
            "Where multiple causes might interact, explain these relationships clearly. "
            "Include specific references to the metrics and patterns that support each diagnosis."
        ),
        agent=agent,
        context=context
    )

def create_impact_assessment_task(agent, context=None):
    """Create a task for assessing the impact of detected anomalies on user experience."""
    return Task(
        description=(
            "Evaluate the potential impact of each diagnosed network anomaly on user "
            "experience and overall 5G modem performance. Determine which anomalies "
            "pose the greatest risk to critical aspects of network operation and "
            "which are likely to be most noticeable to users.\n\n"
            "Consider different use cases such as video streaming, gaming, VoIP calls, "
            "web browsing, and IoT applications, and assess how each anomaly might "
            "affect these different usage scenarios. Prioritize the anomalies based "
            "on their severity, scope of impact, and effect on key performance indicators."
        ),
        expected_output=(
            "A prioritized impact assessment for each anomaly, describing its specific "
            "effects on different aspects of user experience and modem functionality. "
            "The assessment should classify impacts by severity (critical, major, minor) "
            "and affected domains (latency-sensitive applications, throughput-dependent "
            "services, reliability, etc.). Include both immediate impacts and potential "
            "long-term consequences if issues remain unresolved."
        ),
        agent=agent,
        context=context
    )
