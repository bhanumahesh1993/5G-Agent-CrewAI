from crewai import Task

def create_ux_impact_analysis_task(agent, context=None):
    """Create a task for analyzing how network issues impact user experience."""
    return Task(
        description=(
            "Analyze how the identified network anomalies and performance issues "
            "would impact different aspects of user experience. Consider various "
            "user activities such as video streaming, online gaming, video conferencing, "
            "web browsing, file downloads, IoT applications, and voice calls.\n\n"
            "For each type of user activity, assess how the specific network "
            "characteristics and anomalies would manifest in terms of observable "
            "user experience issues such as buffering, lag, pixelation, call drops, "
            "slow loading times, or connection failures. Quantify the severity and "
            "frequency of these issues based on the network data."
        ),
        expected_output=(
            "A comprehensive analysis of user experience impacts, organized by user "
            "activity type. For each activity, detail the specific user-observable "
            "issues that would result from the network anomalies, along with severity "
            "ratings, frequency estimates, and the relationship between technical "
            "metrics and perceived quality. Include a prioritized list of the most "
            "significant user experience problems that should be addressed first."
        ),
        agent=agent,
        context=context
    )

def create_predictive_issue_prevention_task(agent, context=None):
    """Create a task for developing strategies to predict and prevent latency spikes and connection issues."""
    return Task(
        description=(
            "Develop predictive strategies to identify potential latency spikes or "
            "connection issues before they impact users. Focus on early warning "
            "indicators and patterns in the network data that could signal impending "
            "problems.\n\n"
            "Consider how various metrics might show subtle changes before major "
            "issues occur, and how these early indicators could be used to trigger "
            "preventive actions. Include both immediate reactive measures and "
            "longer-term predictive algorithms that could be implemented in the modem's "
            "firmware to anticipate and mitigate problems before users notice them."
        ),
        expected_output=(
            "A detailed set of predictive strategies that includes: early warning "
            "indicators for different types of issues, detection thresholds, "
            "confidence metrics, recommended preventive actions, and implementation "
            "approaches. Each strategy should specify how to detect potential issues "
            "early enough to prevent user impact, what actions to take when warning "
            "signs appear, and how to validate the effectiveness of preventive measures."
        ),
        agent=agent,
        context=context
    )

def create_user_adaptive_optimization_task(agent, context=None):
    """Create a task for developing user-adaptive optimization recommendations."""
    return Task(
        description=(
            "Develop recommendations for how the 5G modem could adapt its behavior "
            "based on learned user patterns to optimize power efficiency, network "
            "selection, and performance. Consider how the modem could intelligently "
            "adjust its operation based on user behaviors, usage patterns, and "
            "application requirements.\n\n"
            "Focus on creating a personalized experience that anticipates user needs "
            "and optimizes network parameters accordingly. Consider techniques such as "
            "usage pattern recognition, application-specific optimizations, location-based "
            "adaptations, and time-of-day adjustments that could enhance user experience "
            "while maximizing modem efficiency."
        ),
        expected_output=(
            "A set of user-adaptive optimization recommendations that includes: "
            "detectable user patterns, corresponding optimization approaches, "
            "learning mechanisms, adaptation parameters, and expected user experience "
            "improvements. Each recommendation should specify what aspects of user "
            "behavior to monitor, how to adapt modem parameters based on these behaviors, "
            "and how these adaptations would enhance the user experience while "
            "potentially improving power efficiency and network performance."
        ),
        agent=agent,
        context=context
    )
