import time
import datetime
import json
import csv
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import bert_score
import logging
import matplotlib.pyplot as plt
from tqdm import tqdm
import click

# Disable warning messages from transformers
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

# defined a global dictionary
bench_data={}


def load_data_from_file(file_path):
    if file_path.endswith('.json'):
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    elif file_path.endswith('.csv'):
        df_data = pd.read_csv(file_path)
        input_csv_data = {}
        input_csv_data['user_id'] = input("Enter user_id: ")
        input_csv_data['project_id'] = input("Enter project_id: ")
        input_csv_data['model_id'] = input("Enter model_id: ")
        input_csv_data['prompts'] = df_data['Prompts'].tolist()
        input_csv_data['types'] = df_data['Types'].tolist()
        input_csv_data['reference_list'] = df_data['Reference List'].tolist()
        return input_csv_data
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")

def load_json(file_path):
    if file_path.endswith('.json'):
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")


def generate_prompt_responses(input_data, pipe, model_load_time, tokenizer_load_time, pipeline_load_time):
    # Initialize the dictionary to store results from running each prompt in the LLM specified in the model_id
    epoch_record = {}

    # Loop through the prompts and generate text
    for i, prompt in enumerate(input_data['prompts']):
        start_time = time.time()
        generated = pipe(prompt, num_return_sequences=1)[0]['generated_text']
        end_time = time.time()
        generation_time = end_time - start_time

        # Store the results in a dictionary record
        record = {
            'timestamp': start_time,
            'project_id': input_data['project_id'],
            'user_id': input_data['user_id'],
            'model_id': input_data['model_id'],
            'prompt': prompt,
            'type': input_data['types'][i],
            'reference_answer': input_data['reference_list'][i],
            'generated_answer': generated,
            'generation_time': generation_time,
            'model_load_time': model_load_time,
            'tokenizer_load_time': tokenizer_load_time,
            'pipeline_load_time': pipeline_load_time,
        }

        # Calculate BERTScore
        P, R, F1 = bert_score.score([generated], [record['reference_answer']], lang="en", verbose=False)
        record['precision'] = P.numpy()[0].item()
        record['recall'] = R.numpy()[0].item()
        record['f1'] = F1.numpy()[0].item()

        # Store the record in epoch_record with a unique key
        epoch_record[f"Example {i + 1}"] = record

    # Return the generated epoch_record dictionary
    return epoch_record

def print_output(epoch_record):
    # Get the timestamp for the current run
    current_timestamp = time.time()

    # Print the common fields only once
    print("Model:", epoch_record["Example 1"]["model_id"])
    print("Project:", epoch_record["Example 1"]["project_id"])
    print("User:", epoch_record["Example 1"]["user_id"])
    print("Run Date:", datetime.datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    print("Model load time:", round(epoch_record["Example 1"]["model_load_time"], 5))
    print("Tokenizer load time:", round(epoch_record["Example 1"]["tokenizer_load_time"], 5))
    print("Pipeline load time:", round(epoch_record["Example 1"]["pipeline_load_time"], 5))
    print("=" * 30)

    # Loop through the examples and print the rest of the fields
    for example_number, record in epoch_record.items():
        print(f"{example_number}:")
        print("Prompt:", record['prompt'])
        print("Generated Text:", record['generated_answer'])
        print("Reference Answer:", record['reference_answer'])
        print("Generation Time:", round(record['generation_time'], 5))
        print("Type:", record['type'])
        print("Precision:", round(record['precision'], 5))
        print("Recall:", round(record['recall'], 5))
        print("F1 Score:", round(record['f1'], 5))
        print("=" * 10)

def print_output_to_file(epoch_record):
    with open("printed_output.txt", "w") as output_file:
        # Get the timestamp for the current run
        current_timestamp = time.time()

        # Write the common fields only once
        output_file.write(f"Model: {epoch_record['Example 1']['model_id']}\n")
        output_file.write(f"Project: {epoch_record['Example 1']['project_id']}\n")
        output_file.write(f"User: {epoch_record['Example 1']['user_id']}\n")
        output_file.write("Run Date: " + datetime.datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S') + "\n")
        output_file.write("Model load time: " + str(round(epoch_record["Example 1"]["model_load_time"], 5)) + "\n")
        output_file.write("Tokenizer load time: " + str(round(epoch_record["Example 1"]["tokenizer_load_time"], 5)) + "\n")
        output_file.write("Pipeline load time: " + str(round(epoch_record["Example 1"]["pipeline_load_time"], 5)) + "\n")
        output_file.write("=" * 30 + "\n")

        # Loop through the examples and write the rest of the fields
        for example_number, record in epoch_record.items():
            output_file.write(f"{example_number}:\n")
            output_file.write("Prompt: " + record.get('prompt', 'N/A') + "\n")
            output_file.write("Generated Text: " + record.get('generated_answer', 'N/A') + "\n")
            output_file.write("Reference Answer: " + record.get('reference_answer', 'N/A') + "\n")
            output_file.write("Generation Time: " + str(round(record['generation_time'], 5)) + "\n")
            output_file.write("Type: " + record.get('type', 'N/A') + "\n")
            output_file.write("Precision: " + str(round(record['precision'], 5)) + "\n")
            output_file.write("Recall: " + str(round(record['recall'], 5)) + "\n")
            output_file.write("F1 Score: " + str(round(record['f1'], 5)) + "\n")
            output_file.write("=" * 10 + "\n")


def plot_data(epoch_record):
    # Lists to store data for the plots
    prompt_types = []
    generation_times = []
    precisions = []
    recalls = []
    f1_scores = []
    # Loop through epoch_record to collect data
    for example_number, record in epoch_record.items():
        prompt_types.append(record['type'])
        generation_times.append(record['generation_time'])
        precisions.append(record['precision'])
        recalls.append(record['recall'])
        f1_scores.append(record['f1'])
        
    # Plot 1: Prompt Types vs. Prompt Generation Times
    plt.figure(figsize=(10, 6))
    plt.bar(prompt_types, generation_times)
    plt.xlabel('Prompt Types')
    plt.ylabel('Generation Time (seconds)')
    plt.title('Prompt Types vs. Prompt Generation Times')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    # Plot Prompt Types vs. BERTScores (Precision, Recall, F1)
    plt.figure(figsize=(10, 6))
    width = 0.2
    x = range(len(prompt_types))
    
    plt.bar(x, precisions, width=width, label='Precision')
    plt.bar([i + width for i in x], recalls, width=width, label='Recall')
    plt.bar([i + 2 * width for i in x], f1_scores, width=width, label='F1 Score')
    
    plt.xlabel('Prompt Types')
    plt.ylabel('Scores')
    plt.title('Prompt Types vs. BERTScores (Precision, Recall, F1)')
    plt.xticks([i + width for i in x], prompt_types, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

def save_output_to_markdown(epoch_record):
    with open("output.md", "w") as md_file:
        # Write the common fields only once
        md_file.write(f"# Model: {epoch_record['Example 1']['model_id']}\n")
        md_file.write(f"Project: {epoch_record['Example 1']['project_id']}\n")
        md_file.write(f"User: {epoch_record['Example 1']['user_id']}\n")
        md_file.write("Run Date: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + "\n")
        md_file.write("Model load time: " + str(round(epoch_record["Example 1"]["model_load_time"], 5)) + "\n")
        md_file.write("Tokenizer load time: " + str(round(epoch_record["Example 1"]["tokenizer_load_time"], 5)) + "\n")
        md_file.write("Pipeline load time: " + str(round(epoch_record["Example 1"]["pipeline_load_time"], 5)) + "\n")
        md_file.write("=" * 30 + "\n\n")

        # Loop through the examples and write the rest of the fields
        for example_number, record in epoch_record.items():
            md_file.write(f"## {example_number}\n")
            md_file.write("Prompt: " + record.get('prompt', 'N/A') + "\n")
            md_file.write("Generated Text: " + record.get('generated_answer', 'N/A') + "\n")
            md_file.write("Reference Answer: " + record.get('reference_answer', 'N/A') + "\n")
            md_file.write("Generation Time: " + str(round(record['generation_time'], 5)) + "\n")
            md_file.write("Type: " + record.get('type', 'N/A') + "\n")
            md_file.write("Precision: " + str(round(record['precision'], 5)) + "\n")
            md_file.write("Recall: " + str(round(record['recall'], 5)) + "\n")
            md_file.write("F1 Score: " + str(round(record['f1'], 5)) + "\n")
            md_file.write("=" * 10 + "\n\n")

def main():
    # Initialize input_data dictionary
    input_data = {}
    valid_choices = ['1', '2', '3']

    while True:
        # Ask the user to choose the input data source
        print("Would you like to run the Reasoning Workbench with the sample data or your own provided JSON or CSV file?")
        print("Enter '1' for sample data, '2' for JSON, or '3' for CSV:")
        user_choice = input()
        print()

        if user_choice in valid_choices:
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Load data based on user choice
    if user_choice == '1':
        # Use the sample data dictionary
        input_data = {
            "user_id": "jbottum",
            "project_id": "project1",
            "model_id": "google/flan-t5-large",
            "prompts": [
                'What is the capital of Germany?',
                'What is the capital of Spain?',
                'What is the capital of Canada?',
                'What is the next number in the sequence: 2, 4, 6, 8, ...? If all cats have tails, and Fluffy is a cat, does Fluffy have a tail?',
                'If you eat too much junk food, what will happen to your health? How does smoking affect the risk of lung cancer?',
                'In the same way that pen is related to paper, what is fork related to? If tree is related to forest, what is brick related to?',
                'Every time John eats peanuts, he gets a rash. Does John have a peanut allergy? Every time Sarah studies for a test, she gets an A. Will Sarah get an A on the next test if she studies?',
                'All dogs have fur. Max is a dog. Does Max have fur? If it is raining outside, and Mary does not like to get wet, will Mary take an umbrella?',
                'If I had studied harder, would I have passed the exam? What would have happened if Thomas Edison had not invented the light bulb?',
                'The center of Tropical Storm Arlene, at 02/1800 UTC, is near 26.7N 86.2W. This position is about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet.  Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida.  Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea.   Where and when will the storm make landfall?',
            ],  # Sample prompts list
            "types": [
                'Knowledge Retrieval',
                'Knowledge Retrieval',
                'Knowledge Retrieval',
                'Logical Reasoning',
                'Cause and Effect',
                'Analogical Reasoning',
                'Inductive Reasoning',
                'Deductive Reasoning',
                'Counterfactual Reasoning',
                'In Context'
            ],    # Sample types list
            "reference_list": [
                'The capital of Germany is Berlin',
                'The capital of Spain is Madrid',
                'The capital of Canada is Ottawa',
                'The next number in the sequence is 10.  Yes, Fluffy is a cat and therefore has a tail.',
                'Eating junk food can result in health problems like weight gain and high cholesterol. Smoking can cause lung issues including cancer.',
                'Fork is related to a plate.  A brick is related to a building.',
                'Maybe, to determine if Johns rash is caused by peanuts, he should take an allergy test for peanuts.   Maybe, Sarah will likely do well if she studies and she may be able to get an A.',
                'Yes, Max is a dog and has fur.   Yes, Mary will take an umbrella.',
                'Yes, if you studied harder, you would have passed the test.  If Thomas Edison did not invent the light blub, another inventor would have created the light bulb.',
                'If Arlene continues in the same direction and speed, the storm will make landfall in the Florida Keys in 18 hours from this report.'
            ]  # Sample reference list
        }
    elif user_choice == '2':
        json_file_path = input("Enter the path to your JSON file: ")
        input_data = load_data_from_file(json_file_path)
    elif user_choice == '3':
        csv_file_path = input("Enter the path to your CSV file: ")
        input_data = load_data_from_file(csv_file_path)
    else:
        print("Invalid choice. Please try again.")

    print("Setting up environment, loading models and generating responses...")
    print()

    with tqdm(total=4, desc="Loading Models", bar_format="{desc}: {percentage:3.0f}%|{bar:20}{r_bar}") as pbar:

        # Load tokenizer, model, and pipeline, and store those loading times
        pbar.set_description_str("Loading Tokenizer")
        tokenizer_start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(input_data['model_id'])
        tokenizer_end_time = time.time()
        pbar.update(1)

        pbar.set_description_str("Loading Model")
        model_start_time = time.time()
        model = AutoModelForSeq2SeqLM.from_pretrained(input_data['model_id'])
        model_end_time = time.time()
        pbar.update(1)

        pbar.set_description_str("Creating Pipeline")
        pipe_start_time = time.time()
        pipe = pipeline(task='text2text-generation', model=model, tokenizer=tokenizer, max_length=512)
        pipe_end_time = time.time()
        pbar.update(1)

        model_load_time = model_end_time - model_start_time
        tokenizer_load_time = tokenizer_end_time - tokenizer_start_time
        pipeline_load_time = pipe_end_time - pipe_start_time

        # Generate prompt responses and collect data
        pbar.set_description_str("Generating responses")
        epoch_record = generate_prompt_responses(input_data, pipe, model_load_time, tokenizer_load_time, pipeline_load_time)
        pbar.update(1)

    valid_choices = ['1', '2', '3', '4', '5','6']
    print()

    while True:
        print("Select the output options (for multiple options, separate by comma e.g. 1,2):")
        print("1. Output report to console")
        print("2. Output to printed_output.txt file")
        print("3. Plots of load times and generation times")
        print("4. epoch_record.csv file")
        print("5. epoch_record.json file")
        print("6. output.md Markdown file")  
        user_output_choice = input().strip()
        user_output_choices = user_output_choice.split(',')

        if all(choice in valid_choices for choice in user_output_choices):
            break
        else:
            print("Invalid choice. Please try again.")
    
    print()

    if '1' in user_output_choice:
        print_output(epoch_record)

    if '2' in user_output_choice:
        print_output_to_file(epoch_record)

    if '3' in user_output_choice:
        plot_data(epoch_record)

    if '4' in user_output_choice:
        # Convert epoch_record to DataFrame and save as CSV
        df = pd.DataFrame.from_dict(epoch_record, orient='index')
        df.to_csv("epoch_record.csv", index=False)

    if '5' in user_output_choice:
        # Save epoch_record as JSON
        with open("epoch_record.json", "w") as jsonfile:
            json.dump(epoch_record, jsonfile)
    if '6' in user_output_choice:
        # Save output to Markdown
        save_output_to_markdown(epoch_record)

def bench_run(json_file_path):
    global bench_data
    # Initialize input_data dictionary

    input_data = load_data_from_file(json_file_path)

    print("Setting up environment, loading models and generating responses...")
    print()

    with tqdm(total=4, desc="Loading Models", bar_format="{desc}: {percentage:3.0f}%|{bar:20}{r_bar}") as pbar:

        # Load tokenizer, model, and pipeline, and store those loading times
        pbar.set_description_str("Loading Tokenizer")
        tokenizer_start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(input_data['model_id'])
        tokenizer_end_time = time.time()
        pbar.update(1)

        pbar.set_description_str("Loading Model")
        model_start_time = time.time()
        model = AutoModelForSeq2SeqLM.from_pretrained(input_data['model_id'])
        model_end_time = time.time()
        pbar.update(1)

        pbar.set_description_str("Creating Pipeline")
        pipe_start_time = time.time()
        pipe = pipeline(task='text2text-generation', model=model, tokenizer=tokenizer, max_length=512)
        pipe_end_time = time.time()
        pbar.update(1)

        model_load_time = model_end_time - model_start_time
        tokenizer_load_time = tokenizer_end_time - tokenizer_start_time
        pipeline_load_time = pipe_end_time - pipe_start_time

        # Generate prompt responses and collect data
        pbar.set_description_str("Generating responses")
        epoch_record = generate_prompt_responses(input_data, pipe, model_load_time, tokenizer_load_time, pipeline_load_time)
        pbar.update(1)

    bench_data = epoch_record

    return epoch_record


def bench_print(print_options):
    global bench_data
    if 'con' in print_options:
        print_output(bench_data)
    if 'txt' in print_options:
        print_output_to_file(bench_data)
    if 'plot' in print_options:
        plot_data(bench_data)
    if 'csv' in print_options:
        # Convert epoch_record to DataFrame and save as CSV
        df = pd.DataFrame.from_dict(bench_data, orient='index')
        df.to_csv("epoch_record.csv", index=False)
    if 'json' in print_options:
        # Save epoch_record as JSON
        with open("epoch_record.json", "w") as jsonfile:
            json.dump(bench_data, jsonfile)
    if 'md' in print_options:
        # Save output to Markdown
        save_output_to_markdown(bench_data)
    if not any(option in print_options for option in ['con', 'txt', 'plot', 'csv', 'json', 'md']):
        print("Invalid output choice. Valid choices: con, txt, plot, csv, json, md.")


@click.command()
@click.option('--run', help='Run the Reasoning Workbench using a JSON file as input.')
@click.option('--print', 'print_options', help='Print output based on user choice (con, txt, csv, json, plot, md).')
def cli(run, print_options):
    if run:
        epoch_record = bench_run(run)
        if print_options:
            print_options = print_options.split(',')
            bench_print(print_options)
        else:
            print("Please provide valid output options using the '--print' option.")

if __name__ == "__main__":
    cli()
