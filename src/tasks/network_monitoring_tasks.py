from crewai import Task

def create_network_data_collection_task(agent):
    """Create a task for collecting network data from PCAP files."""
    return Task(
        description=(
            "Analyze the provided PCAP file to extract comprehensive 5G modem "
            "performance metrics. Extract detailed data on latency, throughput, "
            "signal strength, packet loss, and connection statistics.\n\n"
            "Make sure to look for patterns in the data and specific 5G protocol "
            "information that may indicate the modem's operating conditions. "
            "Process the data systematically and provide a complete set of metrics."
        ),
        expected_output=(
            "A comprehensive JSON structure containing all extracted metrics "
            "including latency statistics (minimum, maximum, average, jitter), "
            "throughput measurements (average and peak), signal strength indicators "
            "(RSSI, SINR), packet loss statistics, and connection establishment metrics. "
            "The data should be well-structured for further analysis."
        ),
        agent=agent
    )

def create_metrics_analysis_task(agent, context=None):
    """Create a task for analyzing collected network metrics."""
    return Task(
        description=(
            "Analyze the collected 5G modem performance metrics to identify "
            "patterns, trends, and notable characteristics. Evaluate the quality "
            "of each performance aspect (latency, throughput, signal strength, etc.) "
            "and determine if they fall within expected ranges for 5G connections.\n\n"
            "Calculate derivative metrics that provide additional insights, such as "
            "stability indicators, performance consistency measurements, and "
            "efficiency metrics."
        ),
        expected_output=(
            "A detailed analysis report containing quality assessments for each "
            "performance aspect, comparative analysis against 5G performance standards, "
            "and identification of potential areas of concern. Include statistical "
            "summaries and derived metrics that provide deeper insights into the "
            "modem's performance characteristics."
        ),
        agent=agent,
        context=context
    )

def create_real_time_metrics_summary_task(agent, context=None):
    """Create a task for summarizing real-time metrics for other agents."""
    return Task(
        description=(
            "Create a concise summary of the most important 5G modem performance "
            "metrics that would be relevant for anomaly detection and optimization. "
            "Focus on the metrics that show unusual patterns or values outside "
            "expected ranges.\n\n"
            "Organize the summary in a way that highlights the most significant "
            "findings first, followed by supporting details. Make sure the summary "
            "provides a complete picture of the current network state."
        ),
        expected_output=(
            "A structured summary of key performance metrics with emphasis on "
            "noteworthy values and patterns. The summary should be comprehensive "
            "yet concise, focusing on information that will be most valuable for "
            "anomaly detection and diagnosis. Include a brief assessment of overall "
            "network health based on the analyzed metrics."
        ),
        agent=agent,
        context=context
    )
