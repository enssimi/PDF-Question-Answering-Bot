import concurrent.futures
import PyPDF2
import openai
import asyncio
import time
import spacy
import warnings
import argparse
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
API_KEY = None


class AnswerCache:
    def __init__(self):
        self.cache = {}

    def get_answer(self, text, question):
        if (text, question) in self.cache:
            return self.cache[(text, question)]
        return None

    def set_answer(self, text, question, answer):
        self.cache[(text, question)] = answer


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    :param pdf_path: Path to the PDF file.
    :return: A list of page texts.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            pages_text = [page.extract_text() for page in reader.pages]
            return pages_text
    except FileNotFoundError:
        raise FileNotFoundError("File not found. Please provide a valid PDF path.")
    except PyPDF2.PdfReadError:
        raise PyPDF2.PdfReadError("Error reading the PDF. Please ensure the file is not corrupted or password-protected.")
    except Exception as e:
        raise Exception("An error occurred while processing the PDF: %s" % str(e))


async def ask_question(text, question, answer_cache):
    """
    Generate an answer for a given question using the OpenAI API.
    :param text: The context text.
    :param question: The question.
    :param answer_cache: Cache to store and retrieve previously generated answers.
    :return: The generated answer.
    """
    try:
        cached_answer = answer_cache.get_answer(text, question)
        if cached_answer:
            return cached_answer

        response = await openai.Completion.create(
            engine='text-davinci-003',
            prompt=f'Context: {text}\nQuestion: {question}\nAnswer:',
            max_tokens=100,
            n=3,  # Number of answers to generate in a single API request
            stop=None,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        answer_cache.set_answer(text, question, answer)
        return answer
    except openai.OpenAIError as e:
        raise openai.OpenAIError("OpenAI API error: %s" % str(e))
    except Exception as e:
        raise Exception("An error occurred while generating the answer: %s" % str(e))


async def batch_process_questions(texts, questions, answer_cache):
    """
    Process a batch of questions using asynchronous processing.
    :param texts: List of context texts.
    :param questions: List of questions.
    :param answer_cache: Cache to store and retrieve previously generated answers.
    :return: List of generated answers.
    """
    loop = asyncio.get_event_loop()
    futures = [loop.create_task(ask_question(text, question, answer_cache)) for text, question in zip(texts, questions)]
    results = []
    for future in asyncio.as_completed(futures):
        try:
            result = await future
            if result:
                results.append(result)
        except Exception as e:
            logger.error("An error occurred while processing a question: %s" % str(e))
    return results


def rank_answers(answers, question, limit=3):
    """
    Rank the answers based on their similarity scores to the question.
    :param answers: List of answers.
    :param question: The question.
    :param limit: Maximum number of answers to return.
    :return: List of ranked answers.
    """
    # Calculate similarity scores between each answer and the question
    scores = [calculate_similarity(answer, question) for answer in answers]

    # Sort the answers based on similarity scores in descending order
    sorted_answers = [answer for _, answer in sorted(zip(scores, answers), reverse=True)]

    # Return the top-ranked answers
    return sorted_answers[:limit]


def calculate_similarity(text1, text2):
    """
    Calculate the similarity score between two texts using spaCy's similarity metric.
    :param text1: The first text.
    :param text2: The second text.
    :return: The similarity score.
    """
    nlp = spacy.load('en_core_web_md')  # Load the spaCy model
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


async def process_pdf(pdf_path, answer_cache):
    """
    Process a PDF file and generate answers for user questions.
    :param pdf_path: Path to the PDF file.
    :param answer_cache: Cache to store and retrieve previously generated answers.
    """
    pdf_texts = extract_text_from_pdf(pdf_path)
    if pdf_texts:
        while True:
            user_question = input("Enter your question (or 'q' to quit): ")
            if user_question.lower() == 'q':
                break

            start_time = time.time()

            answers = await batch_process_questions(pdf_texts, [user_question], answer_cache)

            ranked_answers = rank_answers(answers, user_question)  # Rank the answers

            for answer in ranked_answers:
                print("Answer:", answer)

            end_time = time.time()
            print(f"Processing time: {end_time - start_time} seconds")


def read_api_key_from_config():
    """
    Read the API key from a configuration file or environment variable.
    Modify this function to suit your specific configuration requirements.
    """
    # Example implementation reading from a configuration file
    config_file = "config.ini"
    if os.path.isfile(config_file):
        with open(config_file, "r") as f:
            api_key = f.read().strip()
            return api_key

    # Example implementation reading from an environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDF and answer questions.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    args = parser.parse_args()

    # Read the API key from a configuration file or environment variable
    API_KEY = read_api_key_from_config()

    if not API_KEY:
        raise ValueError("OpenAI API key not provided. Please provide a valid API key.")

    # Initialize the OpenAI API
    openai.api_key = API_KEY

    answer_cache = AnswerCache()

    # Set up the event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_pdf(args.pdf_path, answer_cache))