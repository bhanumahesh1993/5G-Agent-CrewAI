from crewai import Crew, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Import agent creation functions
from ..agents.network_monitoring_agent import create_network_monitoring_agent
from ..agents.anomaly_detection_agent import create_anomaly_detection_agent
from ..agents.optimization_agent import create_optimization_agent
from ..agents.user_experience_agent import create_user_experience_agent
from ..agents.reporting_agent import create_reporting_agent

# Import task creation functions
from ..tasks.network_monitoring_tasks import (
    create_network_data_collection_task,
    create_metrics_analysis_task,
    create_real_time_metrics_summary_task
)
from ..tasks.anomaly_detection_tasks import (
    create_anomaly_detection_task,
    create_diagnostic_analysis_task,
    create_impact_assessment_task
)
from ..tasks.optimization_tasks import (
    create_optimization_strategy_task,
    create_self_healing_recommendations_task,
    create_parameter_tuning_task
)
from ..tasks.user_experience_tasks import (
    create_ux_impact_analysis_task,
    create_predictive_issue_prevention_task,
    create_user_adaptive_optimization_task
)
from ..tasks.reporting_tasks import (
    create_technical_report_task,
    create_performance_visualization_task,
    create_executive_summary_task
)

load_dotenv()

def create_modem_intelligence_crew(verbose=None):
    """
    Create the complete Modem Intelligence Crew with all agents and tasks.
    
    Args:
        verbose (bool, optional): Whether to enable verbose mode
        
    Returns:
        Crew: Configured Modem Intelligence Crew
    """
    # Set verbosity from environment or parameter
    verbose_level = int(os.getenv("VERBOSE_LEVEL", "1")) if verbose is None else verbose
    
    
    # Create all agents
    network_agent = create_network_monitoring_agent(verbose=verbose_level)
    anomaly_agent = create_anomaly_detection_agent(verbose=verbose_level)
    optimization_agent = create_optimization_agent(verbose=verbose_level)
    ux_agent = create_user_experience_agent(verbose=verbose_level)
    reporting_agent = create_reporting_agent(verbose=verbose_level)
    
    # Create all tasks
    # Network monitoring tasks
    network_data_task = create_network_data_collection_task(network_agent)
    metrics_analysis_task = create_metrics_analysis_task(network_agent, [network_data_task])
    metrics_summary_task = create_real_time_metrics_summary_task(network_agent, [metrics_analysis_task])
    
    # Anomaly detection tasks
    anomaly_detection_task = create_anomaly_detection_task(anomaly_agent, [metrics_summary_task])
    diagnostic_task = create_diagnostic_analysis_task(anomaly_agent, [anomaly_detection_task])
    impact_task = create_impact_assessment_task(anomaly_agent, [diagnostic_task])
    
    # Optimization tasks
    optimization_task = create_optimization_strategy_task(optimization_agent, [diagnostic_task, impact_task])
    self_healing_task = create_self_healing_recommendations_task(optimization_agent, [optimization_task])
    parameter_tuning_task = create_parameter_tuning_task(optimization_agent, [self_healing_task])
    
    # User experience tasks
    ux_impact_task = create_ux_impact_analysis_task(ux_agent, [impact_task])
    predictive_task = create_predictive_issue_prevention_task(ux_agent, [ux_impact_task])
    user_adaptive_task = create_user_adaptive_optimization_task(ux_agent, [predictive_task])
    
    # Reporting tasks
    tech_report_task = create_technical_report_task(
        reporting_agent, 
        [metrics_analysis_task, diagnostic_task, optimization_task, user_adaptive_task]
    )
    visualization_task = create_performance_visualization_task(
        reporting_agent,
        [metrics_analysis_task, anomaly_detection_task]
    )
    summary_task = create_executive_summary_task(
        reporting_agent,
        [tech_report_task, visualization_task]
    )
    
    # Create and return the crew
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
    
    crew = Crew(
        agents=[
            network_agent,
            anomaly_agent,
            optimization_agent,
            ux_agent,
            reporting_agent
        ],
        tasks=[
            # Network monitoring tasks
            network_data_task,
            metrics_analysis_task,
            metrics_summary_task,
            
            # Anomaly detection tasks
            anomaly_detection_task,
            diagnostic_task,
            impact_task,
            
            # Optimization tasks
            optimization_task,
            self_healing_task,
            parameter_tuning_task,
            
            # User experience tasks
            ux_impact_task,
            predictive_task,
            user_adaptive_task,
            
            # Reporting tasks
            tech_report_task,
            visualization_task,
            summary_task
        ],
        verbose=verbose_level,
        process=Process.sequential,  # Use sequential process for predictable execution
        manager_llm=ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"), temperature=0.2)  # Lower temperature for more consistent management
    )
    
    return crew
