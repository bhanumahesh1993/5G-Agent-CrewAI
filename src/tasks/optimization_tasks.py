from crewai import Task

def create_optimization_strategy_task(agent, context=None):
    """Create a task for developing optimization strategies for identified issues."""
    return Task(
        description=(
            "Based on the diagnosed network anomalies and their root causes, develop "
            "comprehensive optimization strategies to address each issue. Focus on "
            "practical, effective solutions that could be implemented in a 5G modem "
            "through parameter adjustments, firmware updates, or configuration changes.\n\n"
            "For each strategy, consider the specific mechanisms that would need to be "
            "adjusted, such as dynamic frequency selection, beamforming parameters, "
            "modulation schemes, power control algorithms, or protocol configurations. "
            "Ensure that each strategy addresses the root cause rather than just the symptoms."
        ),
        expected_output=(
            "A detailed set of optimization strategies, with each strategy mapping to "
            "specific diagnosed issues. Each strategy should include: the target issue, "
            "the proposed optimization approach, specific parameters to adjust, expected "
            "outcomes, potential side effects or trade-offs, and implementation priority. "
            "The strategies should be technically sound and specifically applicable to "
            "5G modem operations."
        ),
        agent=agent,
        context=context
    )

def create_self_healing_recommendations_task(agent, context=None):
    """Create a task for developing self-healing recommendations for automated resolution."""
    return Task(
        description=(
            "Develop recommendations for automated self-healing mechanisms that could "
            "be implemented in the 5G modem firmware to automatically detect and resolve "
            "the identified issues without human intervention. Focus on adaptive algorithms "
            "and feedback systems that can continuously monitor performance and make "
            "real-time adjustments.\n\n"
            "Consider how the modem could intelligently adjust its parameters in response "
            "to changing network conditions, interference patterns, or usage demands. "
            "Include specific trigger conditions, adjustment thresholds, and recovery "
            "mechanisms for each recommendation."
        ),
        expected_output=(
            "A set of detailed self-healing recommendations that specify: the targeted "
            "issue, detection mechanisms, trigger conditions, automatic adjustment "
            "parameters, fallback safeguards, and success verification methods. Each "
            "recommendation should be practical for implementation in modem firmware "
            "and should include pseudo-code or algorithmic descriptions where appropriate. "
            "Include explanations of how each mechanism would operate in real-world conditions."
        ),
        agent=agent,
        context=context
    )

def create_parameter_tuning_task(agent, context=None):
    """Create a task for specific parameter tuning recommendations."""
    return Task(
        description=(
            "Provide specific parameter tuning recommendations for the 5G modem to "
            "optimize performance based on the detected issues. Focus on concrete, "
            "actionable parameter adjustments with specific values or ranges that "
            "could be implemented immediately.\n\n"
            "For each parameter, specify the current problematic value or range (if known), "
            "the recommended new value or range, and the expected improvement. Consider "
            "parameters related to radio resource management, power control, link adaptation, "
            "carrier aggregation, MIMO configuration, and protocol timers that are commonly "
            "available in 5G modem firmware."
        ),
        expected_output=(
            "A detailed table of parameter tuning recommendations that includes: parameter "
            "name, current value/setting (if known), recommended value/setting, expected "
            "performance improvement, confidence level, and any dependencies or prerequisites. "
            "The recommendations should be specific enough for direct implementation and "
            "should be prioritized by expected impact. Include explanations of why each "
            "parameter adjustment would help address the identified issues."
        ),
        agent=agent,
        context=context
    )
