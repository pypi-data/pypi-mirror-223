import openai
import pandas as pd

openai.api_key = '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'


def get_summary(report):
    report.context['num_mavics'] = report.detections.drone.str.contains("M2?E").sum()
    report.context['num_matrices'] = report.detections.drone.str.contains("M30").sum()
    if report.context['num_mavics'] > 0:
        report.context['high_prob_koalas'] = len(report.detections)
        report.context['num_validated_koalas'] = (report.detections.gt_outcome == 'verified').sum()
        report.context['num_unvalidated_koalas'] = report.context['high_prob_koalas'] - report.context['num_validated_koalas']
        # if generate_summary:
        #     print('Generating ChatGPT summary...')
        #     report.context['summary'] = generate_summary(detections_df, animal)


def generate_summary(detections_df, animal):
    detections_df['date'] = pd.to_datetime(detections_df['date']).dt.strftime('%-d %B %Y')
    koala_summary_df = detections_df[['date', 'time', 'detection_count', 'gt_outcome', 'gt_method']]
    koala_summary_df.to_csv('koala_summary_df.csv')
    prompt = f"""
    Your task is to take a Pandas DataFrame and summarise the information into natural sounding sentences. For each 
    unique date in the DataFrame write one sentence summarising the information in all entries corresponding to that 
    date. Make sure the <detection_count> value is always paired with the <time> value from the same row and make sure 
    to include every date entry in the table when summarising a specific date. When I mention <animal> I am referring to 
    {animal}. Write all sentences in a single paragraph. When mentioning <time>, use am instead of AM and pm
    instead of PM. An  example of what a sentence could look like is shown below delimited by triple backticks:
    ```On <date>, <detection_count> high probability <animal> were detected between <earliest time for this date> and 
    <latest time for this date>, <gt_outcome> of which were verified.```
    Another example of what a sentence might look like is shown below delimited by triple backticks:
    ```<detection_count> high probability <animal> were detected on <date> at dawn. <gt_outcome> of these were field 
    verfied by pilots.```
    
    DataFrame to summarise: <{koala_summary_df}>
    """
    return get_completion(prompt)


def get_completion(prompt, temperature=0):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'user', 'content': prompt}],
        temperature=temperature,
    )
    return response.choices[0].message['content']
