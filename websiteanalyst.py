import csv
from googlesearch import search
import openai
from tqdm import tqdm

def add_csv_extension(file_name):
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    return file_name

def google_search(query, num_results, file_name):
    # Add .csv extension if not provided
    file_name = add_csv_extension(file_name)

    search_results = search(query, num_results=num_results, lang='en')

    # Create a list to store the results
    results_list = []

    # Iterate through the search results and add them to the list
    for i, result in enumerate(search_results, start=1):
        results_list.append(result)

    # Save the results to a CSV file
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Website'])
        for result in results_list:
            writer.writerow([result])

    print(f"\nSearch results saved to {file_name}")
    return file_name

def get_website_links_from_csv(file_name):
    website_links = []
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            website_links.append(row[0])
    return website_links

def analyze_website(link):
    api_key = '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'  # Replace with your OpenAI API key
    openai.api_key = api_key

    prompt = f"As a website developer, what are the potential problems with the website: {link}?"
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=100,
        temperature=0.6,
        n=1,
        stop=None
    )
    problems = response.choices[0].text.strip()
    return problems

def save_results_to_csv(results, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Website', 'Problems'])
        writer.writerows(results)

# Main code execution
if __name__ == "__main__":
    # Code header
    print("===============================================")
    print("Website Analysis Code by Ranantesh")
    print("Hidden Name: H@cker")
    print("===============================================\n")

    # User inputs
    query = input("Enter your search query: ")
    num_results = int(input("Enter the number of search results: "))
    file_name = input("Enter the file name to save the search results: ")

    # Perform Google search and save the results to a CSV file
    csv_file_name = google_search(query, num_results, file_name)

    # Read website links from the CSV file
    website_links = get_website_links_from_csv(csv_file_name)

    # Output file name for saving the analysis results
    output_file_name = input("Enter the output CSV file name to save the analysis results: ")

    # Analyze each website and save the results to a CSV file
    results = []
    for link in tqdm(website_links, desc="Analyzing Websites"):
        problems = analyze_website(link)
        results.append([link, problems])

    save_results_to_csv
    