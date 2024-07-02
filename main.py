import os
import sys
import time
from api_interaction import send_message, receive_messages
from command_processing import parse_command, process_command

def main():
    print("Current Working Directory:", os.getcwd())
    print("System Path:", sys.path)

    while True:  # Infinite loop to keep running the code
        messages = receive_messages()
        print("Received Messages:", messages)

        for message in messages:
            if 'envelope' in message:
                envelope = message['envelope']
                print("Envelope:", envelope)
                
                # Check if the message is from the allowed source numbers
                source_number = envelope.get('source')
                allowed_numbers = ['PHONE', 'PHONE']
                
                if source_number in allowed_numbers:
                    if 'dataMessage' in envelope and 'message' in envelope['dataMessage']:
                        text = envelope['dataMessage']['message']
                    elif 'syncMessage' in envelope and 'sentMessage' in envelope['syncMessage'] and 'message' in envelope['syncMessage']['sentMessage']:
                        text = envelope['syncMessage']['sentMessage']['message']
                    else:
                        text = None
                    
                    if text:
                        print("Message Text:", text)
                        command = parse_command(text)
                        if command:
                            response = process_command(command)
                            recipients = ["PHONE"]  # Respond to the source number
                            send_message(response, recipients)
                    else:
                        print("Message Text is None or not found")
                else:
                    print(f"Message from {source_number} is not from an allowed number")

        time.sleep(3)  # Wait for 3 seconds before running again

if __name__ == "__main__":
    main()
