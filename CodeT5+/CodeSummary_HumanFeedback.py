import streamlit as st
import json
import csv
from collections import defaultdict
import os

def load_data(uploaded_file):
    data = defaultdict(list)  # Use a dict to group data by file
    for line in uploaded_file:
        item = json.loads(line.decode('utf-8'))
        file_name = os.path.basename(item['file_path'])  # Extract file name
        data[file_name].append(item)  # Group by file name
    return data

# Function to save feedback to CSV
def save_feedback_to_csv(feedback_data):
    csv_file = "feedback_results.csv"
    headers = ['file', 'file_path', 'hash', 'feedback']

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the header
        for file, items in feedback_data.items():
            for data in items:
                # Only write rows where feedback is not 'Select an option'
                if data['feedback'] != 'Select an option':
                    writer.writerow([data['file_path'], data['hash'], data['feedback']])

# Streamlit app
def main():
    st.title('Code Summary Evaluation')

    uploaded_file = st.file_uploader("Choose a JSONL file", type=['jsonl'])
    feedback_data = defaultdict(list)

    if uploaded_file is not None:
        grouped_data = load_data(uploaded_file)

        for file, items in grouped_data.items():
            with st.expander(f"File: {file}", expanded=False):
                for idx, item in enumerate(items):
                    chunk_title = f"Code Chunk {idx + 1}"
                    with st.container():
                        st.write(f"#### {chunk_title}")
                        st.text(f"File Path: {item['file_path']}")
                        st.text(f"Hash: {item['hash']}")
                        st.code(item['code_chunk'], language='python')
                        st.write(f"**Summary:** {item['summary']}")

                        # Adding a default 'Select an option' choice
                        feedback_options = ['Select an option', 'Yes', 'No', 'Needs Improvement']
                        feedback = st.radio(
                            "Is this a good summary for the above code chunk?",
                            options=feedback_options,
                            index=0,  # Default to 'Select an option'
                            key=f'feedback_{file}_{idx}'
                        )

                        feedback_data[file].append({
                            'file_path': item['file_path'],
                            'hash': item['hash'],
                            'feedback': feedback
                        })

        if st.button('Submit All Feedback'):
            save_feedback_to_csv(feedback_data)
            st.success("Feedback submitted successfully!")
            st.balloons()

if __name__ == "__main__":
    main() 