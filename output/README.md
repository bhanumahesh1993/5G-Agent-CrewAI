# Output Directory

This directory stores the results of 5G modem performance analysis generated by the Modem Intelligence Crew.

## Output Files

After running the analysis, this directory will contain:

1. **PDF Reports**: Comprehensive reports containing performance analysis, anomaly detection, and optimization recommendations
2. **JSON Data**: Structured data files containing raw analysis results
3. **Log Files**: Detailed logs of the analysis process
4. **Visualizations**: Charts and graphs depicting various aspects of modem performance

## Organization

By default, each analysis run creates files with timestamps in their names to avoid overwriting previous results.

## Usage

The output files are designed to be human-readable and can be shared with engineering teams for further analysis and action.

The PDF reports are particularly valuable for:
- Understanding overall modem performance
- Identifying specific issues affecting connectivity
- Implementing recommended optimizations
- Tracking performance improvements over time

## Configuration

You can specify a different output directory by:

1. Setting the `OUTPUT_DIR` variable in your `.env` file
2. Using the `--output-dir` command line argument when running the application

Example:
```
python src/main.py --output-dir /path/to/custom/output
```
