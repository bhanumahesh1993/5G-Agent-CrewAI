# Data Directory

This directory contains input data files for the 5G Modem Intelligence Crew.

## Required Files

Place your PCAP files in this directory for analysis. The default configuration looks for a file named `free5gc-compose.pcap`.

## File Format

The system is designed to work with standard PCAP (Packet Capture) files containing 5G network traffic. These files can be captured using tools like Wireshark, tcpdump, or similar network packet capture utilities.

## Configuration

You can specify a different PCAP file by:

1. Setting the `PCAP_FILE_PATH` variable in your `.env` file
2. Using the `--pcap` command line argument when running the application

Example:
```
python src/main.py --pcap data/my_custom_capture.pcap
```

## Sample Data

If you don't have a real 5G network capture, you can use publicly available sample 5G PCAP files for testing purposes. Some sources for sample files include:

- Wireshark's sample captures repository
- Public telecom research datasets
- 5G test environment captures

Note that the analysis quality depends on the contents of the PCAP file. Files should ideally include a complete set of 5G network transactions to enable comprehensive analysis.
