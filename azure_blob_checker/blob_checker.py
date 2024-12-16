import argparse
import csv
import concurrent.futures
from azure.storage.blob import BlobServiceClient
from tabulate import tabulate
import os
import time
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def check_blob_existence(blob_service_client, container_name, filename):
    """
    Check if a blob exists in the specified container.
    
    Args:
        blob_service_client (BlobServiceClient): Azure Blob Service Client
        container_name (str): Name of the container
        filename (str): Name of the blob to check
    
    Returns:
        dict: Dictionary with filename and existence status
    """
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(filename)
        exists = blob_client.exists()
        return {
            'FILENAME': filename,
            'Exists': 'Yes' if exists else 'No'
        }
    except Exception as e:
        return {
            'FILENAME': filename,
            'Exists': 'Error',
            'Error': str(e)
        }

def process_csv_with_blob_check(connection_string, container_name, csv_path, export_format=None):
    """
    Process CSV and check blob existence with concurrent processing.
    
    Args:
        connection_string (str): Azure Storage connection string
        container_name (str): Name of the container
        csv_path (str): Path to the input CSV file
        export_format (str, optional): Format to export results
    """
    # Start timing
    start_time = time.time()
    
    # Print initial processing message
    print(f"{Fore.CYAN}Starting Azure Blob Existence Check{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Container:{Style.RESET_ALL} {container_name}")
    print(f"{Fore.GREEN}Input CSV:{Style.RESET_ALL} {csv_path}")
    
    # Create Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Read input CSV
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Prepare data for concurrent processing
        input_data = list(reader)
    
    total_files = len(input_data)
    print(f"{Fore.YELLOW}Total files to check:{Style.RESET_ALL} {total_files}")
    
    # Concurrent blob existence check
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Create a future for each filename
        futures = {
            executor.submit(
                check_blob_existence, 
                blob_service_client, 
                container_name, 
                row['FILENAME']
            ): row for row in input_data
        }
        
        # Collect results
        results = []
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            original_row = futures[future]
            try:
                existence_result = future.result()
                # Merge original row with existence result
                merged_row = {**original_row, **existence_result}
                results.append(merged_row)
            except Exception as e:
                merged_row = {**original_row, 'Exists': 'Error', 'Error': str(e)}
                results.append(merged_row)
            
            # Progress update
            completed += 1
            print(f"{Fore.BLUE}Checking:{Style.RESET_ALL} {completed}/{total_files} files", end='\r')
    
    # Sort results for consistent display
    results.sort(key=lambda x: x['FILENAME'])
    
    # Calculate summary
    existing_count = sum(1 for r in results if r['Exists'] == 'Yes')
    non_existing_count = sum(1 for r in results if r['Exists'] == 'No')
    error_count = sum(1 for r in results if r['Exists'] == 'Error')
    
    # Clear progress line
    print(" " * 50, end='\r')
    
    # Display non-existing blobs
    non_existing_results = [
        result for result in results 
        if result.get('Exists') == 'No'
    ]
    
    if non_existing_results:
        print(f"\n{Fore.RED}Non-Existing Blobs:{Style.RESET_ALL}")
        print(tabulate(
            [(r['FILENAME'], r['Exists']) for r in non_existing_results], 
            headers=['Filename', 'Exists'], 
            tablefmt='simple'
        ))
    
    # Final Summary
    print("\n" + "=" * 50)
    print(f"{Fore.GREEN}Check Summary:{Style.RESET_ALL}")
    print(f"Total Files Checked:    {total_files}")
    print(f"{Fore.GREEN}Existing Blobs:        {existing_count}{Style.RESET_ALL}")
    print(f"{Fore.RED}Non-Existing Blobs:    {non_existing_count}{Style.RESET_ALL}")
    if error_count > 0:
        print(f"{Fore.YELLOW}Errors:                {error_count}{Style.RESET_ALL}")
    
    # Calculate and display time taken
    end_time = time.time()
    print(f"\n{Fore.CYAN}Time Taken:{Style.RESET_ALL} {end_time - start_time:.2f} seconds")
    
    # Export to CSV if requested (export everything)
    if export_format == 'csv':
        export_path = os.path.splitext(csv_path)[0] + '_blob_check.csv'
        
        # Determine headers - use original CSV headers plus Exists
        if results:
            headers = list(results[0].keys())
            
            with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(results)
            print(f"\n{Fore.GREEN}Results exported to:{Style.RESET_ALL} {export_path}")
    
    return results

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Azure Blob Existence Checker')
    parser.add_argument('connection_string', help='Azure Storage Connection String')
    parser.add_argument('container_name', help='Azure Storage Container Name')
    parser.add_argument('csv_path', help='Path to CSV file with FILENAME column')
    parser.add_argument('-export', choices=['csv'], help='Export results to CSV')
    
    args = parser.parse_args()
    
    # Call processing function
    process_csv_with_blob_check(
        args.connection_string, 
        args.container_name, 
        args.csv_path, 
        args.export
    )

if __name__ == '__main__':
    main()