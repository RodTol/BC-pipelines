import os
import subprocess
import requests

def merge_files(input_dir, output_file):
    file_pattern = "*.fastq"
    with open(output_file, 'w') as outfile:
        for file_name in sorted(os.listdir(input_dir)):
            with open(os.path.join(input_dir, file_name), 'r') as infile:
                outfile.write(infile.read())

def run_nanoplot(input_fastq, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    command = ["NanoPlot", "-t", "2", "--fastq", input_fastq, "-o", output_dir]
    subprocess.run(command)   

# Send report to telegram bot             
def telegram_send_file(path_to_file, caption) :
    token = str(os.environ.get('BC_TOKEN_BOT'))
    chat_id = "-4270864261"
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    files = {'document': open(path_to_file, 'rb')}
    data = {'chat_id': chat_id,'caption': caption}
    results = requests.post(url, files=files, data=data)
    
    if results.status_code == 200:
        print('Message sent successfully!')
    else:
        error_message = f'Failed to send message. Status code: {results.status_code}, Response: {results.text}'
        print(error_message)   