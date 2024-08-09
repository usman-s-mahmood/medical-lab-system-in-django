import pandas as pd
import numpy as np
from faker import Faker
from random import randint
import uuid
from reportlab.lib.pagesizes import letter
import reportlab.pdfgen.canvas as canvas

def main():
    fake = Faker()
    headers = np.array(    
        [
            'patient_id',
            'patient_name',
            'phone_number',
            'email',
            'test_type',
            'result'
        ]
    )
    size = int(input("Enter the size of dataset: "))
    test_type = input('Enter test type: ')
    dataset = pd.DataFrame(
        {
            headers[0]: np.array([i for i in range(1, size+1)]),
            headers[1]: np.array([fake.name() for _ in range(size)]),
            headers[2]: np.array([fake.phone_number() for _ in range(size)]),
            headers[3]: np.array([fake.email() for _ in range(size)]),
            headers[4]: np.array([f'{test_type}' for i in range(0, size)]),
            headers[5]: np.array([randint(10, 100) for i in range(0, size)])
        }
    )
    print(dataset)
    save = input('Do you want to save this dataset in an excel file(Y/N): ')
    if save == 'Y' or save == 'y':
        name = uuid.uuid1()
        dataset.to_excel(f'{test_type}-{name}.xlsx')
        print(f'Dataset is saved with filename: {test_type}-{name}.xlsx')
    elif save == 'N' or save == 'n':
        print(f'Dataset discarded!')
    else:
        print(f'Invalid Option! Dataset discarded')
    # dataset.to_excel('dataset.xlsx')
    
if __name__ == '__main__':
    main()