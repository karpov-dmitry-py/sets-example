import logging
import random
import string
from collections import defaultdict


class SetsHandler:
    SOURCE = 'source.txt'
    RESULT = 'results.txt'
    START_INT = 10 ** 10 - 2 * 10 ** 5
    END_INT = 10 ** 10 - 1
    SOURCE_SIZE = 10 ** 6

    def __init__(self):
        self.set_logger()
        self.result = defaultdict(list)

    def set_logger(self):
        logger = logging.getLogger('sets-handler')
        logger.setLevel(logging.INFO)

        logging_handler = logging.StreamHandler()
        logging_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging_handler.setFormatter(formatter)

        logger.addHandler(logging_handler)
        SetsHandler.logger = logger

    @staticmethod
    def log(msg):
        SetsHandler.logger.info(msg)

    def phone_generator(self):
        return f'+7{str(random.randint(self.START_INT, self.END_INT))}'

    def text_generator(self, size=50, source_string=string.ascii_letters):
        return ''.join(random.choices(source_string, k=size))

    def generate_source(self):
        self.log('generating source data...')
        with open(self.SOURCE, 'w') as dest:
            for counter in range(1, self.SOURCE_SIZE + 1):
                if not counter % 10 ** 5:
                    self.log(f'{counter} of {self.SOURCE_SIZE}...')
                phone = self.phone_generator()
                text = self.text_generator()
                line = f'{phone}\t{text}\n'
                dest.write(line)

    def process_source(self):
        self.log('processing source data...')

        # read source
        with open(self.SOURCE) as source:
            index = 0
            for line in source:
                index += 1
                try:
                    line = line.strip().split('\t')
                    phone, text = line[0], line[1]
                except ValueError:
                    pass
                self.result[phone].append(text)
                if not index % 10 ** 5:
                    self.log(f'processing {index}...')

        # write results
        self.log(f'Writing results to: {self.RESULT}...')
        with open(self.RESULT, 'w') as dest:
            for phone, msgs in self.result.items():
                dest.write(f'Phone number: {phone}. Total messages: {len(msgs)}\n')
                for msg in msgs:
                    dest.write(f'\t*** {msg}\n')

        self.log(f'Total unique phone numbers in results: {len(self.result.keys())}')

    @staticmethod
    def time_tracker(func):
        import time

        def decorated(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = round(time.time() - start_time, 2)
            SetsHandler.log(f'Done! Total duration: {duration} sec(s).')
            return result

        return decorated


@SetsHandler.time_tracker
def main():
    handler = SetsHandler()
    handler.generate_source()
    handler.process_source()


if __name__ == '__main__':
    main()
