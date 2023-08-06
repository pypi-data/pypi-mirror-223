# Reason Workbench

- [Reason_workbench readme](#reason_workbench-readme)
  * [Library Installation via pip3](#library-installation-via-pip3)
  * [Usage](#usage)
    + [Start script - GCP Colab Notebook](#start-script---gcp-colab-notebook)
    + [Start script - from python3 enable command line](#start-script---from-python3-enable-command-line)
    + [After starting script, select your data input choice](#after-starting-script-select-your-data-input-choice)
    + [Processing time and status message](#processing-time-and-status-message)
  * [Output options](#output-options)
  * [Input_data dictionary](#input_data-dictionary)
  * [Prompt processing](#prompt-processing)
    + [Explanation of the BERTScore processing](#explanation-of-the-bertscore-processing)
    + [Definition of Percision, Recall and F1](#definition-of-percision-recall-and-f1)
  * [Input data customization](#input-data-customization)
  * [Inputing custom data into the JSON format](#inputing-custom-data-into-the-json-format)
    + [JSON schema (for input file):](#json-schema-for-input-file)
      - [Field details and explanation](#field-details-and-explanation)
  * [Using custom input data in data.csv format](#using-custom-input-data-in-datacsv-format)
    + [CSV Schema (for input file):](#csv-schema-for-input-file)
  * [input_data dictionary example](#input_data-dictionary-example)
  * [Output report to console or txt file](#output-report-to-console-or-txt-file)
  * [Epoch record data (CSV format)](#epoch-record-data-csv-format)
  * [Epoch record data (JSON format)](#epoch-record-data-json-format)
  * [Markdown output](#markdown-output)
  * [Complete example of installation and all output options using the sample data in a colab notebook](#complete-example-of-installation-and-all-output-options-using-the-sample-data-in-a-colab-notebook)
  * [Plot examples](#plot-examples)
  * [Appendix - Results with flan-T5-xl, using Google colab with A100 GPU](#appendix---results-with-flan-t5-xl-using-google-colab-with-a100-gpu)
  * [Results for flan-T5-xxL with GCP colab using A100 GPU](#results-for-flan-t5-xxl-with-gcp-colab-using-a100-gpu)

# Reason_workbench readme 

Reason workbench is a Python library, installed via 'pip3 install reason_workbench', that provides a process to perform customized validation of Large Language Models (LLMs), especially for the LLM's reasoning capabilities.  The library processes a set of questions (prompts) and generates answers through text generation by the LLM.   It provides automated BERTScoring of the LLM's answers based on reference answers supplied in the input data set.  It provides the user options for 5 types of ouput: text ouput to console, text output to file, plots, JSON epoch_record file, and CSV epoch_record file.   The user is prompted to selected one or more of these output options.  The script runs on your local machine and/or in a jupyter notebook such as GCP's colab.  

From a data input standpoint, the library asks the user to select the source of the input data.  The three input data choices are to use the sample data or to have the user provide a JSON or CVS file, e.g. data.json or data.csv.  For option 1, the script offers a sample data set.  The sample data set includes a list of prompts to ask the LLM.  This data set includes six types of reasoning questions.   The data set also includes lists for prompt types and for the corresponding reference answers.   

For option 2 or 3, the script offers the user the ability to upload their own set of prompts, prompt types and reference answers in the JSON or CSV file, via a schema that is provided below.   If user provided data is selected, the script will ask for the path to the file (which must include the file name and extension).  If JSON is selected, a few other fields are expected in the input schedule e.g. model_id, project_id, user_id.  If CSV is selected, the CSV provides the prompts, types and reference answers, and the scripts prompts the users to enter the model_id, project_id, user_id.  Please note the  project_id and user_id fields are not required.   These fields help to keep track of epoch_runs and may be used to integrate with the upcoming reasoning engine.  The library has been tested with model_id = "google/flan-t5-large" and "google/flan-T5-base" with a free version of GCP colab using a CPU.   The library has been tested with others T5 model variants i.e. "google/flan-t5-xl" and "google/flan-t5-xxl" with a GCP colab with a A100 GPU, which costs a fee. After the input data is selected and provided, an input_data dictionary is created and loaded with data based on the user's input.   The prompt processing begins.

From a prompt processing and epoch recoord output standpoint, the script processses each prompt in the input_data dictionary.   After generating and scoring the answer to the prompt, the script creates an epoch record that contains 15 fields that include the prompt, the reference answer, the LLM generated answer, generation time and the BERTScore, which compare the reference answer to the generated answer.   These 8 fields, along with 7 others, are stored in two epoch_record dictionary.  

In addition to the epoch_record dictionary, the script also prompts the user to select from the script's ouput types.  The output types include - Text ouput to console, Text ouput to file, Plots, CSV file or JSON file.  Multiple options can be selected by answersing with commas between the numbers associated with the optins.  The Text output to console and the Text output to file provide the the 15 fields in the epoch record results from each prompt, along with the details of the model, user, project and load times. These files are nanmed epoch_record.csv and epoch_record.json.    

The following sections provide more details on the script's installation, usage, the input_data dictionary, prompt processing, input data customization along with examples of the printed text based output, and the input and the output file schemas.


## Library Installation via pip3
The library is designed to be installed via pip3 in your python envirnonment (python 3.11) using this command from your terminal.
```
pip install reason_workbench
```
Note - running in a GCP colab notebook, please use "!pip install reason_workbench"

The installation includes all the scripts and dependencies needed for the library.  The dependencies include:
```
transformers>=4.0.0
accelerate>=0.3.0
torch>=1.7.0
bert-score>=0.3.9
```
Running this command will generate this output and you will want to make sure that you see the last line "Successfully installed..."
```
Collecting reason_workbench
  Downloading reason_workbench-0.1.0-py3-none-any.whl (6.0 kB)
Collecting transformers (from reason_workbench)
  Downloading transformers-4.31.0-py3-none-any.whl (7.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.4/7.4 MB 10.7 MB/s eta 0:00:00
Collecting bert-score (from reason_workbench)
  Downloading bert_score-0.3.13-py3-none-any.whl (61 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.1/61.1 kB 4.0 MB/s eta 0:00:00
Requirement already satisfied: pandas in /usr/local/lib/python3.10/dist-packages (from reason_workbench) (1.5.3)
Requirement already satisfied: matplotlib in /usr/local/lib/python3.10/dist-packages (from reason_workbench) (3.7.1)
Requirement already satisfied: torch>=1.0.0 in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (2.0.1+cu118)
Requirement already satisfied: numpy in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (1.22.4)
Requirement already satisfied: requests in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (2.27.1)
Requirement already satisfied: tqdm>=4.31.1 in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (4.65.0)
Requirement already satisfied: packaging>=20.9 in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (23.1)
Requirement already satisfied: python-dateutil>=2.8.1 in /usr/local/lib/python3.10/dist-packages (from pandas->reason_workbench) (2.8.2)
Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.10/dist-packages (from pandas->reason_workbench) (2022.7.1)
Requirement already satisfied: filelock in /usr/local/lib/python3.10/dist-packages (from transformers->reason_workbench) (3.12.2)
Collecting huggingface-hub<1.0,>=0.14.1 (from transformers->reason_workbench)
  Downloading huggingface_hub-0.16.4-py3-none-any.whl (268 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 268.8/268.8 kB 11.1 MB/s eta 0:00:00
Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.10/dist-packages (from transformers->reason_workbench) (6.0.1)
Requirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.10/dist-packages (from transformers->reason_workbench) (2022.10.31)
Collecting tokenizers!=0.11.3,<0.14,>=0.11.1 (from transformers->reason_workbench)
  Downloading tokenizers-0.13.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (7.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.8/7.8 MB 35.2 MB/s eta 0:00:00
Collecting safetensors>=0.3.1 (from transformers->reason_workbench)
  Downloading safetensors-0.3.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 27.2 MB/s eta 0:00:00
Requirement already satisfied: contourpy>=1.0.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (1.1.0)
Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (0.11.0)
Requirement already satisfied: fonttools>=4.22.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (4.41.1)
Requirement already satisfied: kiwisolver>=1.0.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (1.4.4)
Requirement already satisfied: pillow>=6.2.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (9.4.0)
Requirement already satisfied: pyparsing>=2.3.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (3.1.0)
Requirement already satisfied: fsspec in /usr/local/lib/python3.10/dist-packages (from huggingface-hub<1.0,>=0.14.1->transformers->reason_workbench) (2023.6.0)
Requirement already satisfied: typing-extensions>=3.7.4.3 in /usr/local/lib/python3.10/dist-packages (from huggingface-hub<1.0,>=0.14.1->transformers->reason_workbench) (4.7.1)
Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil>=2.8.1->pandas->reason_workbench) (1.16.0)
Requirement already satisfied: sympy in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (1.11.1)
Requirement already satisfied: networkx in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (3.1)
Requirement already satisfied: jinja2 in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (3.1.2)
Requirement already satisfied: triton==2.0.0 in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (2.0.0)
Requirement already satisfied: cmake in /usr/local/lib/python3.10/dist-packages (from triton==2.0.0->torch>=1.0.0->bert-score->reason_workbench) (3.25.2)
Requirement already satisfied: lit in /usr/local/lib/python3.10/dist-packages (from triton==2.0.0->torch>=1.0.0->bert-score->reason_workbench) (16.0.6)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (1.26.16)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (2023.7.22)
Requirement already satisfied: charset-normalizer~=2.0.0 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (2.0.12)
Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (3.4)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from jinja2->torch>=1.0.0->bert-score->reason_workbench) (2.1.3)
Requirement already satisfied: mpmath>=0.19 in /usr/local/lib/python3.10/dist-packages (from sympy->torch>=1.0.0->bert-score->reason_workbench) (1.3.0)
Installing collected packages: tokenizers, safetensors, huggingface-hub, transformers, bert-score, reason_workbench
Successfully installed bert-score-0.3.13 huggingface-hub-0.16.4 reason_workbench-0.1.0 safetensors-0.3.1 tokenizers-0.13.3 transformers-4.31.0
```

## Usage

### Start script - GCP Colab Notebook
If running in a colab notebook, after the packages are installed, please run this import command.

```
from reason_workbench import main
```
After this import completes, you can start the script via this commmmand.  Important, you must run the import command above before running this command.
```
main.main()
```

### Start script - from python3 enable command line

After install, please run this statement

``` 
reason_workbench
```

### After starting script, select your data input choice

After running either the colab or console command(s) above, you will see the following prompt:

```
Would you like to run the Reasoning Workbench with the sample data or your own provided JSON or CSV file? 
Enter '1' for sample data, '2' for JSON, or '3' for CSV:
```

If you enter 1, the script will run with its predefined input data.  The script generates an evaluation of a set of sample prompts for the predefined model (flan-T5-large). The sample prompts and reference answers are primarily designed to provide a quick evaluation of the LLM's reasoning capabilities.  It also tests questions for knowledge retrieval and a complex in-context question.  The script uses BERTScore (Recall, Precision and F1) to measure the generated answer to the reference answer.  It provides you with six forms of output: print to console, txt, plots, json, csv and md files.  This option demonstrates that the script is functional from input to procesing to output.  

The example data can help those who want to develop custom input data.  The script takes the data that is provided in the python data dictionary and creates a JSON and a CSV file.  The JSON file is then used to reload the data into the python data dictionary.   These examples show that input data can be ingested in JSON and CSV formats.   

If you enter 2 or 3, you can enter custom input data in JSON or CSV formats and the details, includes the schemas, are reviewed in the upcoming sections.

### Processing time and status message

After you make your selection, you will receive a set of progress message.   The prompt generation does typically take a few minutes.
```
Setting up environment, loading models and generating responses...

Generating responses: 100%|████████████████████| 4/4 [01:55<00:00, 28.82s/it]
```
## Output options

After the responses are generated you will be prompted to select your output options
```
Select the output options (for mulitple options, separate by comma e.g. 1,2:
1. Output report to console
2. Output report to txt file
3. Plots of load times and generation times
4. epoch_record.csv file
5. epoch_record.json file
6. output.md Markdown file  
```
If you enter 1,2,3, you will get a print output to console, txt file of ouput, and a JSON file in the epoch_record.json file schema.  Each of these output schemas are defined below and examples are also provided.

A complete example of installation and all output options using the sample data in a colab notebook is provided at the end of this post.

## Input_data dictionary 
The script uses a data dictionary (input_data) to store variables for processsing.   The input_data dictionary can be loaded from script's predefined data or via a JSON or CSV file (data.json or data.csv).  The dictionary and example data values are provided below.

```
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
],  

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
],   
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
    'If Arlene continues in the same direciton and speed, storm will make landfall in the Forida Keys in 18 hours from this report.'
]
```
Note - For option 1, the script builds an example json and csv files (data.json and csv.json) and then reloads that same data into the input_data dictionary.   We provided this process to validate that the CVS and JSON file formats will work.  

## Prompt processing
The script access the input_data dictionary and loops through the list of prompts.  For each prompt, it generates a text answer to each prompt by the LLM model. The script then automatically calculates the BertScore by comparing the LLM's generated answer to the reference answers. The scoring methods include Precision, Recall, and F1.

Each prompt is processed and recorded separately in a epoch record. Each epoch record is stored in both the epoch_record.csv and the epoch_record.json. For each prompt, the script also produces a printed text output of 15 fields with 8 fields about the project and model and 7 about the prompt generation details.   An example of the output is provided [here](##text-output).

The following provides the actual code for the loop and some explanation.

```
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
        'project_name': input_data['project_id'],
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
```

Explanation of the answer generation process for the generated variable

The code takes each input prompt from the input_data['prompts'] list, feeds it to the text generation pipeline (pipe), and stores the generated text in the generated variable. The time taken to generate the text is also recorded using start_time and end_time variables. The variable generation_time then stores the time taken for the generation process.  The following reviews the top fields used in the loop.

prompt: This is an individual input prompt for which the text generation is performed. The input_data['prompts'] is the list containing multiple input prompts.

pipe: This refers to the text generation pipeline for the language model (in this case flan-T5-Large). The pipe function is invoked with the prompt as its input.

num_return_sequences: This parameter specifies the number of sequences (text responses) that should be generated for each input prompt. In this case, it's set to 1, which means only one text sequence will be generated for each input prompt.

generated = pipe(prompt, num_return_sequences=1)[0]['generated_text']: The output of the pipe function is a list of generated sequences (text). Since num_return_sequences is set to 1, the generated output is a list with one element. The code then selects the first (and only) element of this list using [0].  It then accesses the 'generated_text' key from the selected dictionary to get the actual generated text.

### Explanation of the BERTScore processing

P, R, F1 = bert_score.score([generated], [record['reference_answer']], lang="en", verbose=False): This line invokes a function named score from the BERTScore library. BERTScore is a metric used to evaluate the quality of generated text compared to reference text using BERT embeddings. It quantifies the similarity between the generated answer and the reference answer.

Input Parameters:

generated: This variable contains the text generated by the language model for the current input prompt.
record['reference_answer']: This retrieves the reference answer (ground truth) associated with the current prompt from the record dictionary. The record dictionary seems to contain various details related to the generated text, reference text, and other metadata.
lang="en": This parameter specifies the language of the text. In this case, it is set to "en" for English.

verbose=False: This parameter controls the verbosity of the calculation, and it is set to False, so the function won't produce detailed output.

P, R, F1: These variables are used to store the precision, recall, and F1-score values returned by the bert_score.score function. These metrics indicate how well the generated text matches the reference text.

Storing Results:

record['precision']: This line stores the precision value obtained from the BERTScore calculation into the record dictionary under the key 'precision'.
record['recall']: This line stores the recall value into the record dictionary under the key 'recall'.
record['f1']: This line stores the F1-score value into the record dictionary under the key 'f1'.

After these steps, the record dictionary contains the BERTScore metrics along with other information related to the generated text, reference text, timing, and model details. The record dictionary is then added to the epoch_record dictionary with a unique key (f"Example {i + 1}"), which seems to represent each example's index in the loop.

### Definition of Percision, Recall and F1

Precision is a measure of how many of the generated tokens (words or subwords) are relevant compared to the reference tokens. It indicates the accuracy of the generated text concerning the reference text. A high precision means that the generated text has a low number of irrelevant tokens when compared to the reference text.

Recall is a measure of how many of the reference tokens are covered or matched by the generated tokens. It indicates the comprehensiveness of the generated text in capturing the important information from the reference text. A high recall means that the generated text contains most of the relevant tokens from the reference text.

F1-score is the harmonic mean of precision and recall. It provides a balance between precision and recall, as it takes into account both false positives (low precision) and false negatives (low recall). F1-score is a common metric used in information retrieval tasks, including text generation evaluation, where precision and recall are both important.

## Input data customization
To tailor the evaluation to your specific use case, you can modify the prompts and reference answers in the script. Additionally, you can adjust the model_id variable to use a different LLM model for evaluation.  Please feel free to experiment and adapt the script according to your needs.  

## Inputing custom data into the JSON format

For users who want to use a JSON file to input custom data, the users will need to:

1) create the custom data in the JSON file format. 
2) use option 2 in the initial message to the user
3) provide the full path to the JSON file (including the file name and extension i.e. custom_data.json)

The script will ingest the data and load it into the input_data directory.  It will then run the processing to generate the answers to the prompts and measure the answers.

### JSON schema (for input file):

```
['user_id', 'project_id', 'model_id', 'prompts', 'types', 'reference_list']
```

#### Field details and explanation
```
{ "user_id": "string", "project_id": "string", "model_id": "string", "prompts": [ "string", ... ], "types": [ "string", ... ], "reference_list": [ "string", ... ] }
```
Explanation of the fields

user_id (string): The user_id field is a string that should contain the unique identifier of the user who owns the project. This identifier helps in associating the data with a specific user account or project owner.

project_id (string): The project_id field is a string that should contain the unique identifier of the project associated with the data. It allows users to differentiate between various projects and their corresponding data.

model_id (string): The model_id field is a string that should contain the identifier of the model used for the project. This identifier helps users identify the specific language model or AI model used for processing the prompts.

prompts (list of strings): The prompts field is a list of strings. Each string in this list represents a different type of question or scenario that the model is expected to answer or process. Users should provide the prompts in the order they want them processed.

types (list of strings): The types field is a list of strings. Each string in this list corresponds to the type of the prompt in the same position in the prompts list. The types categorize the prompts based on their nature, such as "Knowledge Retrieval," "Logical Reasoning," etc.

reference_list (list of strings): The reference_list field is a list of strings. Each string in this list corresponds to the example reference answer for the prompt in the same position in the prompts list. These reference answers represent the expected model responses for each prompt.

Note:

The ... in the schema represents that the respective lists (prompts, types, and reference_list) can contain an arbitrary number of elements, depending on the number of prompts and their corresponding information. Users building JSON files should follow the exact structure and field names as specified in the schema to ensure compatibility and proper data representation within the app.


## Using custom input data in data.csv format

When the user selects option 3, the user can ingest prompts, types and reference answers using a CSV ingestion in the script.  This ingestion does not include the model_id, project_id or user_id.  The script prompts the user to input those values.   The script also asks the user to provide the full path to the CSV file (which should include the full path, filename and extension).

### CSV Schema (for input file):
```
['Prompts', 'Types', 'Reference List']
```
More details and explanations:
```
Prompts,Types,Reference List string,string,string ...
```
Explanation

Prompts (string): This column should contain the prompts that represent different types of questions or scenarios for the model to answer or process. 
Types (string): This column should contain the types corresponding to each prompt. These types categorize the prompts based on the nature of the question or scenario, such as "Knowledge Retrieval," "Logical Reasoning," etc. 
Reference List (string): This column should contain the example reference answers for each prompt. These reference answers represent the expected model responses to the corresponding prompts. 

Note: The ... in the schema indicates that there can be an arbitrary number of rows in the CSV file, each corresponding to a different prompt, type, and reference answer. Users building CSV files should strictly follow the order of columns as specified in the schema to ensure proper mapping and accuracy. Each row in the CSV should contain data for one prompt, its corresponding type, and the reference answer.


## input_data dictionary example

The data will need to be converted from those formats to the input_data dictionary.   For reference, here is the input_data dictionary with the sample data.

```
{'user_id': 'jbottum', 'project_id': 'project1', 'model_id': 'google/flan-t5-large', 'prompts': ['What is the capital of Germany?', 'What is the capital of Spain?', 'What is the capital of Canada?', 'What is the next number in the sequence: 2, 4, 6, 8, ...? If all cats have tails, and Fluffy is a cat, does Fluffy have a tail?', 'If you eat too much junk food, what will happen to your health? How does smoking affect the risk of lung cancer?', 'In the same way that pen is related to paper, what is fork related to? If tree is related to forest, what is brick related to?', 'Every time John eats peanuts, he gets a rash. Does John have a peanut allergy? Every time Sarah studies for a test, she gets an A. Will Sarah get an A on the next test if she studies?', 'All dogs have fur. Max is a dog. Does Max have fur? If it is raining outside, and Mary does not like to get wet, will Mary take an umbrella?', 'If I had studied harder, would I have passed the exam? What would have happened if Thomas Edison had not invented the light bulb?', 'The center of Tropical Storm Arlene, at 02/1800 UTC, is near 26.7N 86.2W. This position is about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet.  Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida.  Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea.   Where and when will the storm make landfall?'], 'types': ['Knowledge Retrieval', 'Knowledge Retrieval', 'Knowledge Retrieval', 'Logical Reasoning', 'Cause and Effect', 'Analogical Reasoning', 'Inductive Reasoning', 'Deductive Reasoning', 'Counterfactual Reasoning', 'In Context'], 'reference_list': ['The capital of Germany is Berlin', 'The capital of Spain is Madrid', 'The capital of Canada is Ottawa', 'The next number in the sequence is 10.  Yes, Fluffy is a cat and therefore has a tail.', 'Eating junk food can result in health problems like weight gain and high cholesterol. Smoking can cause lung issues including cancer.', 'Fork is related to a plate.  A brick is related to a building.', 'Maybe, to determine if Johns rash is caused by peanuts, he should take an allergy test for peanuts.   Maybe, Sarah will likely do well if she studies and she may be able to get an A.', 'Yes, Max is a dog and has fur.   Yes, Mary will take an umbrella.', 'Yes, if you studied harder, you would have passed the test.  If Thomas Edison did not invent the light blub, another inventor would have created the light bulb.', 'If Arlene continues in the same direciton and speed, storm will make landfall in the Forida Keys in 18 hours from this report.']}
```

## Output report to console or txt file

The following provides a sample of the text file output the script.  This format is the same for the print to console and print to file.  The content is also the same for the Markdown output option.

```
Model: google/flan-t5-large
Project: project1
User: jbottum
Run Date: 2023-07-24 11:55:47
Model load time: 27.52373
Tokenizer load time: 0.39852
Pipeline load time: 0.11755
==============================
Example 1:
Prompt: What is the capital of Germany?
Generated Text: berlin
Reference Answer: The capital of Germany is Berlin
Generation Time: 1.98715
Type: Knowledge Retrieval
Precision: 0.80484
Recall: 0.82159
F1 Score: 0.81313
==========
Example 2:
Prompt: What is the capital of Spain?
Generated Text: turin
Reference Answer: The capital of Spain is Madrid
Generation Time: 0.96034
Type: Knowledge Retrieval
Precision: 0.76089
Recall: 0.79643
F1 Score: 0.77825
==========
Example 3:
Prompt: What is the capital of Canada?
Generated Text: toronto
Reference Answer: The capital of Canada is Ottawa
Generation Time: 0.94883
Type: Knowledge Retrieval
Precision: 0.77874
Recall: 0.78587
F1 Score: 0.78229
==========
Example 4:
Prompt: What is the next number in the sequence: 2, 4, 6, 8, ...? If all cats have tails, and Fluffy is a cat, does Fluffy have a tail?
Generated Text: yes
Reference Answer: The next number in the sequence is 10.  Yes, Fluffy is a cat and therefore has a tail.
Generation Time: 1.01579
Type: Logical Reasoning
Precision: 0.80039
Recall: 0.80802
F1 Score: 0.80419
==========
Example 5:
Prompt: If you eat too much junk food, what will happen to your health? How does smoking affect the risk of lung cancer?
Generated Text: no
Reference Answer: Eating junk food can result in health problems like weight gain and high cholesterol. Smoking can cause lung issues including cancer.
Generation Time: 0.75727
Type: Cause and Effect
Precision: 0.8171
Recall: 0.79509
F1 Score: 0.80595
==========
Example 6:
Prompt: In the same way that pen is related to paper, what is fork related to? If tree is related to forest, what is brick related to?
Generated Text: brick is related to brick
Reference Answer: Fork is related to a plate.  A brick is related to a building.
Generation Time: 1.54485
Type: Analogical Reasoning
Precision: 0.92856
Recall: 0.89745
F1 Score: 0.91274
==========
Example 7:
Prompt: Every time John eats peanuts, he gets a rash. Does John have a peanut allergy? Every time Sarah studies for a test, she gets an A. Will Sarah get an A on the next test if she studies?
Generated Text: yes
Reference Answer: Maybe, to determine if Johns rash is caused by peanuts, he should take an allergy test for peanuts.   Maybe, Sarah will likely do well if she studies and she may be able to get an A.
Generation Time: 1.3012
Type: Inductive Reasoning
Precision: 0.82268
Recall: 0.7907
F1 Score: 0.80638
==========
Example 8:
Prompt: All dogs have fur. Max is a dog. Does Max have fur? If it is raining outside, and Mary does not like to get wet, will Mary take an umbrella?
Generated Text: yes
Reference Answer: Yes, Max is a dog and has fur.   Yes, Mary will take an umbrella.
Generation Time: 1.08936
Type: Deductive Reasoning
Precision: 0.80579
Recall: 0.80846
F1 Score: 0.80712
==========
Example 9:
Prompt: If I had studied harder, would I have passed the exam? What would have happened if Thomas Edison had not invented the light bulb?
Generated Text: no one would have invented the light bulb
Reference Answer: Yes, if you studied harder, you would have passed the test.  If Thomas Edison did not invent the light blub, another inventor would have created the light bulb.
Generation Time: 1.83537
Type: Counterfactual Reasoning
Precision: 0.90208
Recall: 0.86655
F1 Score: 0.88395
==========
Example 10:
Prompt: The center of Tropical Storm Arlene, at 02/1800 UTC, is near 26.7N 86.2W. This position is about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet.  Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida.  Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea.   Where and when will the storm make landfall?
Generated Text: about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba
Reference Answer: If Arlene continues in the same direciton and speed, storm will make landfall in the Forida Keys in 18 hours from this report.
Generation Time: 10.48913
Type: In Context
Precision: 0.79358
Recall: 0.81645
F1 Score: 0.80485
==========

```

## Epoch record data (CSV format) 

The script produces a CSV file with a record created for each prompt processed.  The file is written to the file directory in which the script is run.   The file name is epoch_record.CSV.

The epoch_record.csv schema is:

```
timestamp: Start time of the prompt's processing
project_name: User provided project name, optional
user_id: user provided user id, optional
prompt: The text of the prompt given to the language model.
type: The type of the prompt, such as "knowledge retrieval," "reasoning," or "in-context."
reference_answer: The human-generated reference answer for the prompt.
generated_answer: The answer generated by the language model for the given prompt.
generation_time: The time taken by the language model to generate the answer for the prompt (in seconds).
model_load_time: model_load_time,
tokenizer_load_time: tokenizer_load_time,
pipeline_load_time: pipeline_load_time,
precision: The precision score obtained by comparing the generated answer to the reference answer using BERTScore.
recall: The recall score obtained by comparing the generated answer to the reference answer using BERTScore.
f1: The F1 score obtained by comparing the generated answer to the reference answer using BERTScore.
Example #: unique number associated with each epoch record
```

## Epoch record data (JSON format) 

The script produces a JSON file with a record created for each prompt processed.  The file is written to the file directory in which the script is run.   The file name is epoch_record.JSON.

The schema is provided below:
```
{
  "Example 1": {
    "timestamp": 1690217662.396554,
    "project_name": "project1",
    "user_id": "jbottum",
    "model_id": "google/flan-t5-large",
    "prompt": "What is the capital of Germany?",
    "type": "Knowledge Retrieval",
    "reference_answer": "The capital of Germany is Berlin",
    "generated_answer": "berlin",
    "generation_time": 1.9871528148651123,
    "model_load_time": 27.523733139038086,
    "tokenizer_load_time": 0.39852213859558105,
    "pipeline_load_time": 0.1175541877746582,
    "precision": 0.8048427104949951,
    "recall": 0.821587860584259,
    "f1": 0.8131290674209595
  },
  "Example 2": {
    "timestamp": 1690217679.919581,
    "project_name": "project1",
    "user_id": "jbottum",
    "model_id": "google/flan-t5-large",
    "prompt": "What is the capital of Spain?",
    "type": "Knowledge Retrieval",
    "reference_answer": "The capital of Spain is Madrid",
    "generated_answer": "turin",
    "generation_time": 0.9603440761566162,
    "model_load_time": 27.523733139038086,
    "tokenizer_load_time": 0.39852213859558105,
    "pipeline_load_time": 0.1175541877746582,
    "precision": 0.7608890533447266,
    "recall": 0.7964281439781189,
    "f1": 0.7782530188560486
  },
  // ... (more examples)
}
```

Explanation of the fields:


"Example N": A unique identifier for each example, represented as a string. It can be any descriptive name or index.

"timestamp": The timestamp when the example was evaluated, represented as a floating-point number.

"project_name": The name of the project associated with the evaluation, represented as a string.

"user_id": The user ID or name of the person who conducted the evaluation, represented as a string.

"model_id": The ID or name of the language model used for evaluation, represented as a string.

"prompt": The text of the prompt given to the language model, represented as a string.

"type": The type of the prompt, such as "Knowledge Retrieval," "Logical Reasoning," "Cause and Effect," etc., represented as a string.

"reference_answer": The human-generated reference answer for the prompt, represented as a string.

"generated_answer": The answer generated by the language model for the given prompt, represented as a string.

"generation_time": The time taken by the language model to generate the answer for the prompt, represented as a floating-point number (in seconds).

"model_load_time": The time taken to load the language model, represented as a floating-point number (in seconds).

"tokenizer_load_time": The time taken to load the model's tokenizer, represented as a floating-point number (in seconds).

"pipeline_load_time": The time taken to load the pipeline (if used), represented as a floating-point number (in seconds).

"precision": The precision score obtained by comparing the generated answer to the reference answer using some evaluation metric, represented as a floating-point number.

"recall": The recall score obtained by comparing the generated answer to the reference answer using some evaluation metric, represented as a floating-point number.

"f1": The F1 score obtained by combining precision and recall using some evaluation metric, represented as a floating-point number.


The epoch_record.JSON with the sample data.

```
{'Example 1': {'timestamp': 1690217662.396554, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'What is the capital of Germany?', 'type': 'Knowledge Retrieval', 'reference_answer': 'The capital of Germany is Berlin', 'generated_answer': 'berlin', 'generation_time': 1.9871528148651123, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.8048427104949951, 'recall': 0.821587860584259, 'f1': 0.8131290674209595}, 'Example 2': {'timestamp': 1690217679.919581, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'What is the capital of Spain?', 'type': 'Knowledge Retrieval', 'reference_answer': 'The capital of Spain is Madrid', 'generated_answer': 'turin', 'generation_time': 0.9603440761566162, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.7608890533447266, 'recall': 0.7964281439781189, 'f1': 0.7782530188560486}, 'Example 3': {'timestamp': 1690217686.08467, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'What is the capital of Canada?', 'type': 'Knowledge Retrieval', 'reference_answer': 'The capital of Canada is Ottawa', 'generated_answer': 'toronto', 'generation_time': 0.9488329887390137, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.7787359356880188, 'recall': 0.7858681678771973, 'f1': 0.7822858095169067}, 'Example 4': {'timestamp': 1690217691.639713, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'What is the next number in the sequence: 2, 4, 6, 8, ...? If all cats have tails, and Fluffy is a cat, does Fluffy have a tail?', 'type': 'Logical Reasoning', 'reference_answer': 'The next number in the sequence is 10.  Yes, Fluffy is a cat and therefore has a tail.', 'generated_answer': 'yes', 'generation_time': 1.0157949924468994, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.800387442111969, 'recall': 0.8080228567123413, 'f1': 0.8041870594024658}, 'Example 5': {'timestamp': 1690217698.094964, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'If you eat too much junk food, what will happen to your health? How does smoking affect the risk of lung cancer?', 'type': 'Cause and Effect', 'reference_answer': 'Eating junk food can result in health problems like weight gain and high cholesterol. Smoking can cause lung issues including cancer.', 'generated_answer': 'no', 'generation_time': 0.7572689056396484, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.8171018362045288, 'recall': 0.7950920462608337, 'f1': 0.8059467673301697}, 'Example 6': {'timestamp': 1690217704.132812, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'In the same way that pen is related to paper, what is fork related to? If tree is related to forest, what is brick related to?', 'type': 'Analogical Reasoning', 'reference_answer': 'Fork is related to a plate.  A brick is related to a building.', 'generated_answer': 'brick is related to brick', 'generation_time': 1.5448510646820068, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.9285570383071899, 'recall': 0.8974470496177673, 'f1': 0.9127370119094849}, 'Example 7': {'timestamp': 1690217710.429468, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'Every time John eats peanuts, he gets a rash. Does John have a peanut allergy? Every time Sarah studies for a test, she gets an A. Will Sarah get an A on the next test if she studies?', 'type': 'Inductive Reasoning', 'reference_answer': 'Maybe, to determine if Johns rash is caused by peanuts, he should take an allergy test for peanuts.   Maybe, Sarah will likely do well if she studies and she may be able to get an A.', 'generated_answer': 'yes', 'generation_time': 1.3011960983276367, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.822684109210968, 'recall': 0.7907010316848755, 'f1': 0.8063755631446838}, 'Example 8': {'timestamp': 1690217717.598289, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'All dogs have fur. Max is a dog. Does Max have fur? If it is raining outside, and Mary does not like to get wet, will Mary take an umbrella?', 'type': 'Deductive Reasoning', 'reference_answer': 'Yes, Max is a dog and has fur.   Yes, Mary will take an umbrella.', 'generated_answer': 'yes', 'generation_time': 1.0893568992614746, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.8057858347892761, 'recall': 0.8084622025489807, 'f1': 0.8071218132972717}, 'Example 9': {'timestamp': 1690217723.859654, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'If I had studied harder, would I have passed the exam? What would have happened if Thomas Edison had not invented the light bulb?', 'type': 'Counterfactual Reasoning', 'reference_answer': 'Yes, if you studied harder, you would have passed the test.  If Thomas Edison did not invent the light blub, another inventor would have created the light bulb.', 'generated_answer': 'no one would have invented the light bulb', 'generation_time': 1.8353681564331055, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.9020756483078003, 'recall': 0.8665458559989929, 'f1': 0.8839539289474487}, 'Example 10': {'timestamp': 1690217731.266442, 'project_name': 'project1', 'user_id': 'jbottum', 'model_id': 'google/flan-t5-large', 'prompt': 'The center of Tropical Storm Arlene, at 02/1800 UTC, is near 26.7N 86.2W. This position is about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet.  Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida.  Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea.   Where and when will the storm make landfall?', 'type': 'In Context', 'reference_answer': 'If Arlene continues in the same direciton and speed, storm will make landfall in the Forida Keys in 18 hours from this report.', 'generated_answer': 'about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba', 'generation_time': 10.48912501335144, 'model_load_time': 27.523733139038086, 'tokenizer_load_time': 0.39852213859558105, 'pipeline_load_time': 0.1175541877746582, 'precision': 0.793580174446106, 'recall': 0.8164472579956055, 'f1': 0.8048513531684875}}

```

## Markdown output

If you select option 6, output.md Markdown file, the script will generate an 'output.md' file into the directory that the script is run.   The contents of the data are the same as the printed output in option 1.


## Complete example of installation and all output options using the sample data in a colab notebook

```
!pip install reason_workbench
```

```
Collecting reason_workbench
  Downloading reason_workbench-0.1.0-py3-none-any.whl (6.0 kB)
Collecting transformers (from reason_workbench)
  Downloading transformers-4.31.0-py3-none-any.whl (7.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.4/7.4 MB 10.7 MB/s eta 0:00:00
Collecting bert-score (from reason_workbench)
  Downloading bert_score-0.3.13-py3-none-any.whl (61 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.1/61.1 kB 4.0 MB/s eta 0:00:00
Requirement already satisfied: pandas in /usr/local/lib/python3.10/dist-packages (from reason_workbench) (1.5.3)
Requirement already satisfied: matplotlib in /usr/local/lib/python3.10/dist-packages (from reason_workbench) (3.7.1)
Requirement already satisfied: torch>=1.0.0 in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (2.0.1+cu118)
Requirement already satisfied: numpy in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (1.22.4)
Requirement already satisfied: requests in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (2.27.1)
Requirement already satisfied: tqdm>=4.31.1 in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (4.65.0)
Requirement already satisfied: packaging>=20.9 in /usr/local/lib/python3.10/dist-packages (from bert-score->reason_workbench) (23.1)
Requirement already satisfied: python-dateutil>=2.8.1 in /usr/local/lib/python3.10/dist-packages (from pandas->reason_workbench) (2.8.2)
Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.10/dist-packages (from pandas->reason_workbench) (2022.7.1)
Requirement already satisfied: filelock in /usr/local/lib/python3.10/dist-packages (from transformers->reason_workbench) (3.12.2)
Collecting huggingface-hub<1.0,>=0.14.1 (from transformers->reason_workbench)
  Downloading huggingface_hub-0.16.4-py3-none-any.whl (268 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 268.8/268.8 kB 11.1 MB/s eta 0:00:00
Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.10/dist-packages (from transformers->reason_workbench) (6.0.1)
Requirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.10/dist-packages (from transformers->reason_workbench) (2022.10.31)
Collecting tokenizers!=0.11.3,<0.14,>=0.11.1 (from transformers->reason_workbench)
  Downloading tokenizers-0.13.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (7.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.8/7.8 MB 35.2 MB/s eta 0:00:00
Collecting safetensors>=0.3.1 (from transformers->reason_workbench)
  Downloading safetensors-0.3.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 27.2 MB/s eta 0:00:00
Requirement already satisfied: contourpy>=1.0.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (1.1.0)
Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (0.11.0)
Requirement already satisfied: fonttools>=4.22.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (4.41.1)
Requirement already satisfied: kiwisolver>=1.0.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (1.4.4)
Requirement already satisfied: pillow>=6.2.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (9.4.0)
Requirement already satisfied: pyparsing>=2.3.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->reason_workbench) (3.1.0)
Requirement already satisfied: fsspec in /usr/local/lib/python3.10/dist-packages (from huggingface-hub<1.0,>=0.14.1->transformers->reason_workbench) (2023.6.0)
Requirement already satisfied: typing-extensions>=3.7.4.3 in /usr/local/lib/python3.10/dist-packages (from huggingface-hub<1.0,>=0.14.1->transformers->reason_workbench) (4.7.1)
Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil>=2.8.1->pandas->reason_workbench) (1.16.0)
Requirement already satisfied: sympy in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (1.11.1)
Requirement already satisfied: networkx in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (3.1)
Requirement already satisfied: jinja2 in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (3.1.2)
Requirement already satisfied: triton==2.0.0 in /usr/local/lib/python3.10/dist-packages (from torch>=1.0.0->bert-score->reason_workbench) (2.0.0)
Requirement already satisfied: cmake in /usr/local/lib/python3.10/dist-packages (from triton==2.0.0->torch>=1.0.0->bert-score->reason_workbench) (3.25.2)
Requirement already satisfied: lit in /usr/local/lib/python3.10/dist-packages (from triton==2.0.0->torch>=1.0.0->bert-score->reason_workbench) (16.0.6)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (1.26.16)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (2023.7.22)
Requirement already satisfied: charset-normalizer~=2.0.0 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (2.0.12)
Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests->bert-score->reason_workbench) (3.4)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from jinja2->torch>=1.0.0->bert-score->reason_workbench) (2.1.3)
Requirement already satisfied: mpmath>=0.19 in /usr/local/lib/python3.10/dist-packages (from sympy->torch>=1.0.0->bert-score->reason_workbench) (1.3.0)
Installing collected packages: tokenizers, safetensors, huggingface-hub, transformers, bert-score, reason_workbench
Successfully installed bert-score-0.3.13 huggingface-hub-0.16.4 reason_workbench-0.1.0 safetensors-0.3.1 tokenizers-0.13.3 transformers-4.31.0
```
After the packages are installed, please run this important command:

```
from reason_workbench import main
```

To run the script, enter this command:

```
main.main()
```

```
Would you like to run the Reasoning Workbench with the sample data or your own provided JSON or CSV file?
Enter '1' for sample data, '2' for JSON, or '3' for CSV:
1

Loading Tokenizer:   0%|                    | 0/4 [00:00<?, ?it/s]
Downloading (…)okenizer_config.json: 100%
2.54k/2.54k [00:00<00:00, 155kB/s]
Downloading spiece.model: 100%
792k/792k [00:00<00:00, 9.97MB/s]
Downloading (…)/main/tokenizer.json: 100%
2.42M/2.42M [00:00<00:00, 19.3MB/s]
Downloading (…)cial_tokens_map.json: 100%
2.20k/2.20k [00:00<00:00, 82.9kB/s]
Loading Model:  25%|█████               | 1/4 [00:01<00:05,  1.69s/it]    
Downloading (…)lve/main/config.json: 100%
662/662 [00:00<00:00, 41.0kB/s]
Downloading model.safetensors: 100%
3.13G/3.13G [00:57<00:00, 57.1MB/s]
Downloading (…)neration_config.json: 100%
147/147 [00:00<00:00, 11.0kB/s]
Generating responses:  75%|███████████████     | 3/4 [01:15<00:23, 23.88s/it]
Downloading (…)lve/main/config.json: 100%
482/482 [00:00<00:00, 28.5kB/s]
Downloading (…)olve/main/vocab.json: 100%
899k/899k [00:00<00:00, 11.1MB/s]
Downloading (…)olve/main/merges.txt: 100%
456k/456k [00:00<00:00, 8.03MB/s]
Downloading model.safetensors: 100%
1.42G/1.42G [00:16<00:00, 60.4MB/s]
Generating responses: 100%|████████████████████| 4/4 [02:19<00:00, 34.78s/it]

Select the output options (for mulitple options, separate by comma e.g. 1,2:
1. Printed Output
2. File of Printed Output
3. Plots of Output
4. epoch_record.csv File
5. epoch_record.json File
1,2,3,4,5
Model: google/flan-t5-large
Project: N/A
User: jbottum
Run Date: 2023-08-01 19:37:22
Model load time: 66.14036
Tokenizer load time: 2.04346
Pipeline load time: 0.17913
==============================
Example 2:
Prompt: What is the capital of Spain?
Generated Text: turin
Reference Answer: The capital of Spain is Madrid
Generation Time: 1.54225
Type: Knowledge Retrieval
Precision: 0.76089
Recall: 0.79643
F1 Score: 0.77825
==========
Example 3:
Prompt: What is the capital of Canada?
Generated Text: toronto
Reference Answer: The capital of Canada is Ottawa
Generation Time: 1.05016
Type: Knowledge Retrieval
Precision: 0.77874
Recall: 0.78587
F1 Score: 0.78229
==========
Example 4:
Prompt: What is the next number in the sequence: 2, 4, 6, 8, ...? If all cats have tails, and Fluffy is a cat, does Fluffy have a tail?
Generated Text: yes
Reference Answer: The next number in the sequence is 10.  Yes, Fluffy is a cat and therefore has a tail.
Generation Time: 1.25063
Type: Logical Reasoning
Precision: 0.80039
Recall: 0.80802
F1 Score: 0.80419
==========
Example 5:
Prompt: If you eat too much junk food, what will happen to your health? How does smoking affect the risk of lung cancer?
Generated Text: no
Reference Answer: Eating junk food can result in health problems like weight gain and high cholesterol. Smoking can cause lung issues including cancer.
Generation Time: 0.90212
Type: Cause and Effect
Precision: 0.8171
Recall: 0.79509
F1 Score: 0.80595
==========
Example 6:
Prompt: In the same way that pen is related to paper, what is fork related to? If tree is related to forest, what is brick related to?
Generated Text: brick is related to brick
Reference Answer: Fork is related to a plate.  A brick is related to a building.
Generation Time: 1.8151
Type: Analogical Reasoning
Precision: 0.92856
Recall: 0.89745
F1 Score: 0.91274
==========
Example 7:
Prompt: Every time John eats peanuts, he gets a rash. Does John have a peanut allergy? Every time Sarah studies for a test, she gets an A. Will Sarah get an A on the next test if she studies?
Generated Text: yes
Reference Answer: Maybe, to determine if Johns rash is caused by peanuts, he should take an allergy test for peanuts.   Maybe, Sarah will likely do well if she studies and she may be able to get an A.
Generation Time: 1.21691
Type: Inductive Reasoning
Precision: 0.82268
Recall: 0.7907
F1 Score: 0.80638
==========
Example 8:
Prompt: All dogs have fur. Max is a dog. Does Max have fur? If it is raining outside, and Mary does not like to get wet, will Mary take an umbrella?
Generated Text: yes
Reference Answer: Yes, Max is a dog and has fur.   Yes, Mary will take an umbrella.
Generation Time: 1.04767
Type: Deductive Reasoning
Precision: 0.80579
Recall: 0.80846
F1 Score: 0.80712
==========
Example 9:
Prompt: If I had studied harder, would I have passed the exam? What would have happened if Thomas Edison had not invented the light bulb?
Generated Text: no one would have invented the light bulb
Reference Answer: Yes, if you studied harder, you would have passed the test.  If Thomas Edison did not invent the light blub, another inventor would have created the light bulb.
Generation Time: 2.17448
Type: Counterfactual Reasoning
Precision: 0.90208
Recall: 0.86655
F1 Score: 0.88395
==========
Example 10:
Prompt: The center of Tropical Storm Arlene, at 02/1800 UTC, is near 26.7N 86.2W. This position is about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet.  Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida.  Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea.   Where and when will the storm make landfall?
Generated Text: about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba
Reference Answer: If Arlene continues in the same direction and speed, the storm will make landfall in the Florida Keys in 18 hours from this report.
Generation Time: 12.17895
Type: In Context
Precision: 0.80119
Recall: 0.83572
F1 Score: 0.81809
==========

```

## Plot examples

Plot of the reference answer generation times by prompt types.

![Alt text](gen_times.png)

Plot of bertscores by prompt types.

![Alt text](bertscores.png)


## Appendix - Results with flan-T5-xl, using Google colab with A100 GPU

```
Model: google/flan-t5-xl
Project: N/A
User: jbottum
Run Date: 2023-08-02 22:09:22
Model load time: 69.83294
Tokenizer load time: 1.85772
Pipeline load time: 0.04989
==============================
Example 2:
Prompt: What is the capital of Spain?
Generated Text: santander
Reference Answer: The capital of Spain is Madrid
Generation Time: 1.3377
Type: Knowledge Retrieval
Precision: 0.72719
Recall: 0.80743
F1 Score: 0.76521
==========
Example 3:
Prompt: What is the capital of Canada?
Generated Text: ottawa
Reference Answer: The capital of Canada is Ottawa
Generation Time: 1.00034
Type: Knowledge Retrieval
Precision: 0.75266
Recall: 0.79511
F1 Score: 0.7733
==========
Example 4:
Prompt: What is the next number in the sequence: 2, 4, 6, 8, ...? If all cats have tails, and Fluffy is a cat, does Fluffy have a tail?
Generated Text: yes
Reference Answer: The next number in the sequence is 10.  Yes, Fluffy is a cat and therefore has a tail.
Generation Time: 0.93387
Type: Logical Reasoning
Precision: 0.80039
Recall: 0.80802
F1 Score: 0.80419
==========
Example 5:
Prompt: If you eat too much junk food, what will happen to your health? How does smoking affect the risk of lung cancer?
Generated Text: It increases the risk of developing lung cancer.
Reference Answer: Eating junk food can result in health problems like weight gain and high cholesterol. Smoking can cause lung issues including cancer.
Generation Time: 2.01493
Type: Cause and Effect
Precision: 0.9095
Recall: 0.86195
F1 Score: 0.88509
==========
Example 6:
Prompt: In the same way that pen is related to paper, what is fork related to? If tree is related to forest, what is brick related to?
Generated Text: building
Reference Answer: Fork is related to a plate.  A brick is related to a building.
Generation Time: 0.89609
Type: Analogical Reasoning
Precision: 0.83162
Recall: 0.8084
F1 Score: 0.81984
==========
Example 7:
Prompt: Every time John eats peanuts, he gets a rash. Does John have a peanut allergy? Every time Sarah studies for a test, she gets an A. Will Sarah get an A on the next test if she studies?
Generated Text: yes
Reference Answer: Maybe, to determine if Johns rash is caused by peanuts, he should take an allergy test for peanuts.   Maybe, Sarah will likely do well if she studies and she may be able to get an A.
Generation Time: 0.98186
Type: Inductive Reasoning
Precision: 0.82268
Recall: 0.7907
F1 Score: 0.80638
==========
Example 8:
Prompt: All dogs have fur. Max is a dog. Does Max have fur? If it is raining outside, and Mary does not like to get wet, will Mary take an umbrella?
Generated Text: yes
Reference Answer: Yes, Max is a dog and has fur.   Yes, Mary will take an umbrella.
Generation Time: 1.17275
Type: Deductive Reasoning
Precision: 0.80579
Recall: 0.80846
F1 Score: 0.80712
==========
Example 9:
Prompt: If I had studied harder, would I have passed the exam? What would have happened if Thomas Edison had not invented the light bulb?
Generated Text: the world would be dark
Reference Answer: Yes, if you studied harder, you would have passed the test.  If Thomas Edison did not invent the light blub, another inventor would have created the light bulb.
Generation Time: 1.34182
Type: Counterfactual Reasoning
Precision: 0.83843
Recall: 0.81596
F1 Score: 0.82704
==========
Example 10:
Prompt: The center of Tropical Storm Arlene, at 02/1800 UTC, is near 26.7N 86.2W. This position is about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet.  Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida.  Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea.   Where and when will the storm make landfall?
Generated Text: Fort Myers in Florida
Reference Answer: If Arlene continues in the same direciton and speed, storm will make landfall in the Forida Keys in 18 hours from this report.
Generation Time: 2.09916
Type: In Context
Precision: 0.81611
Recall: 0.79779
F1 Score: 0.80684
==========
```


## Results for flan-T5-xxL with GCP colab using A100 GPU

```

Model: google/flan-t5-xxl
Project: N/A
User: jbottum
Run Date: 2023-08-02 23:09:29
Model load time: 2467.86555
Tokenizer load time: 2.02283
Pipeline load time: 0.10828
==============================
Example 2:
Prompt: What is the capital of Spain?
Generated Text: madrid
Reference Answer: The capital of Spain is Madrid
Generation Time: 2.54445
Type: Knowledge Retrieval
Precision: 0.83004
Recall: 0.82224
F1 Score: 0.82612
==========
Example 3:
Prompt: What is the capital of Canada?
Generated Text: ottawa
Reference Answer: The capital of Canada is Ottawa
Generation Time: 3.66145
Type: Knowledge Retrieval
Precision: 0.75266
Recall: 0.79511
F1 Score: 0.7733
==========
Example 4:
Prompt: What is the next number in the sequence: 2, 4, 6, 8, ...? If all cats have tails, and Fluffy is a cat, does Fluffy have a tail?
Generated Text: yes
Reference Answer: The next number in the sequence is 10.  Yes, Fluffy is a cat and therefore has a tail.
Generation Time: 2.8549
Type: Logical Reasoning
Precision: 0.80039
Recall: 0.80802
F1 Score: 0.80419
==========
Example 5:
Prompt: If you eat too much junk food, what will happen to your health? How does smoking affect the risk of lung cancer?
Generated Text: Smoking increases the risk of lung cancer.
Reference Answer: Eating junk food can result in health problems like weight gain and high cholesterol. Smoking can cause lung issues including cancer.
Generation Time: 5.73978
Type: Cause and Effect
Precision: 0.91666
Recall: 0.86281
F1 Score: 0.88892
==========
Example 6:
Prompt: In the same way that pen is related to paper, what is fork related to? If tree is related to forest, what is brick related to?
Generated Text: building
Reference Answer: Fork is related to a plate.  A brick is related to a building.
Generation Time: 2.716
Type: Analogical Reasoning
Precision: 0.83162
Recall: 0.8084
F1 Score: 0.81984
==========
Example 7:
Prompt: Every time John eats peanuts, he gets a rash. Does John have a peanut allergy? Every time Sarah studies for a test, she gets an A. Will Sarah get an A on the next test if she studies?
Generated Text: yes
Reference Answer: Maybe, to determine if Johns rash is caused by peanuts, he should take an allergy test for peanuts.   Maybe, Sarah will likely do well if she studies and she may be able to get an A.
Generation Time: 2.73718
Type: Inductive Reasoning
Precision: 0.82268
Recall: 0.7907
F1 Score: 0.80638
==========
Example 8:
Prompt: All dogs have fur. Max is a dog. Does Max have fur? If it is raining outside, and Mary does not like to get wet, will Mary take an umbrella?
Generated Text: yes
Reference Answer: Yes, Max is a dog and has fur.   Yes, Mary will take an umbrella.
Generation Time: 2.64937
Type: Deductive Reasoning
Precision: 0.80579
Recall: 0.80846
F1 Score: 0.80712
==========
Example 9:
Prompt: If I had studied harder, would I have passed the exam? What would have happened if Thomas Edison had not invented the light bulb?
Generated Text: the world would be a darker place
Reference Answer: Yes, if you studied harder, you would have passed the test.  If Thomas Edison did not invent the light blub, another inventor would have created the light bulb.
Generation Time: 5.371
Type: Counterfactual Reasoning
Precision: 0.8244
Recall: 0.82028
F1 Score: 0.82233
==========
Example 10:
Prompt: The center of Tropical Storm Arlene, at 02/1800 UTC, is near 26.7N 86.2W. This position is about 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet.  Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida.  Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea.   Where and when will the storm make landfall?
Generated Text: 425 km/230 nm to the west of Fort Myers in Florida, and it is about 550 km/297 nm to the NNW of the western tip of Cuba. The tropical storm is moving southward, or 175 degrees, 4 knots. The estimated minimum central pressure is 1002 mb. The maximum sustained wind speeds are 35 knots with gusts to 45 knots. The sea heights that are close to the tropical storm are ranging from 6 feet to a maximum of 10 feet. Precipitation: scattered to numerous moderate is within 180 nm of the center in the NE quadrant. Isolated moderate is from 25N to 27N between 80W and 84W, including parts of south Florida. Broad surface low pressure extends from the area of the tropical storm, through the Yucatan Channel, into the NW part of the Caribbean Sea. Where and when will the storm make landfall?
Reference Answer: If Arlene continues in the same direciton and speed, storm will make landfall in the Forida Keys in 18 hours from this report.
Generation Time: 94.84838
Type: In Context
Precision: 0.77103
Recall: 0.82801
F1 Score: 0.7985
==========

```