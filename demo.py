from src.pipeline import EduQuery
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', action='store_true', help='enable verbose mode')
args = parser.parse_args()

eq = EduQuery()
while True:
    print('Enter exit to stop')
    question = input('Enter your question: ')
    if question == 'exit':
        break
    try:
        resp = eq.ask(question=question, verbose=args.verbose)
        print('\n', 'Answer:', resp, '\n\n')
    except Exception as e:
        print(e)
