import pandas as pd
import numpy as np
from faker import Faker
from random import choice, randint
import uuid
from gender_guesser.detector import Detector

def get_test_result(test_type):
    ranges = {
        'diabetes': (50, 150),  # Example range, adjust as needed
        'cholesterol': (100, 300),
        'ldl_cholesterol': (50, 200),
        'hdl_cholesterol': (20, 100),
        'triglycerides': (50, 400),
        'bun': (5, 50),
        'alp': (20, 150),
        'calcium': (6, 12),
        'wbc': (2, 15),
    }
    return randint(*ranges[test_type])

def get_gender(name):
    d = Detector()
    gender = d.get_gender(name.split()[0])
    return 'M' if gender in ['male', 'mostly_male'] else 'F'

def main():
    fake = Faker()
    test_types = [
        'diabetes',
        'cholesterol',
        'ldl_cholesterol',
        'hdl_cholesterol',
        'triglycerides',
        'bun',
        'alp',
        'calcium',
        'wbc',
    ]
    size = int(input("Enter the size of dataset: "))
    
    dataset = pd.DataFrame(
        {
            'patient_id': np.array([i for i in range(1, size+1)]),
            'patient_name': np.array([fake.name() for _ in range(size)]),
            'gender': np.array([get_gender(fake.name()) for _ in range(size)]),
            'phone_number': np.array([fake.phone_number() for _ in range(size)]),
            'email': np.array([fake.email() for _ in range(size)]),
            'test_type': np.array([choice(test_types) for _ in range(size)]),
        }
    )
    
    dataset['result'] = dataset.apply(lambda row: get_test_result(row['test_type']), axis=1)
    
    print(dataset)
    
    save = input('Do you want to save this dataset in an excel file (Y/N): ')
    if save.lower() == 'y':
        name = uuid.uuid1()
        dataset.to_excel(f'dataset-{name}.xlsx', index=False)
        print(f'Dataset is saved with filename: dataset-{name}.xlsx')
    else:
        print('Dataset discarded!')

if __name__ == '__main__':
    main()
