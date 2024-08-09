from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
import pandas as pd
import numpy as np
from faker import Faker
from random import randint
import uuid
from reportlab.lib.pagesizes import letter
import reportlab.pdfgen.canvas as canvas
from django.conf import settings
import os
from gender_guesser.detector import Detector
from random import choice, randint
from datetime import datetime, timedelta, date
# Create your views here.

def get_test_result(test_type):
    ranges = {
        'diabetes': (50, 150),
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

def generate_random_dob(size):
    fake = Faker()
    today = datetime.today()
    start_date = today - timedelta(days=75*365)  # 75 years ago
    end_date = today - timedelta(days=18*365)    # 18 years ago
    random_dob = [fake.date_of_birth(minimum_age=18, maximum_age=75) for _ in range(size)]
    return random_dob

def dataset_generator_driver_code(size):
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
    pstat = []
    for _ in range(size):
        if (randint(0, 1) == 1):
            pstat.append('paid')
        else:
            pstat.append('unpaid')
    
    dataset = pd.DataFrame(
        {
            'patient_id': np.array([i for i in range(1, size+1)]),
            'patient_name': np.array([fake.name() for _ in range(size)]),
            'gender': np.array([get_gender(fake.name()) for _ in range(size)]),
            'phone_number': np.array([fake.phone_number() for _ in range(size)]),
            'email': np.array([fake.email() for _ in range(size)]),
            'test_type': np.array([choice(test_types) for _ in range(size)]),
            'date_of_birth': generate_random_dob(size),
            'payment': np.array([randint(5, 10) for _ in range(size)]),
            'payment_status': np.array(pstat)
        }
    )
    
    dataset['result'] = dataset.apply(lambda row: get_test_result(row['test_type']), axis=1)
    
    print(dataset)
    filename = str(f'sample-dataset-{uuid.uuid4()}.xlsx')
    file_dir = os.path.join(settings.MEDIA_ROOT, 'reports', 'sample')
    file_path = os.path.join(file_dir, filename)
    dataset.to_excel(
        file_path, 
        index=False
    )
    return f'/media/reports/sample/{filename}'

def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

def test_evaluation(filename, user):
    try:
        dataset = pd.read_excel(filename)
        for index, row in dataset.iterrows():
            '''
            # for demonstration purposes, these print statements are added to the code 
            print("Patient Name:", row['patient_name'])
            print("Phone Number:", row['phone_number'])
            print("Email:", row['email'])
            print("Test Type:", row['test_type'])
            print("Result:", row['result'])
            print("Date of Birth: ", row['date_of_birth'])
            '''
            age = calculate_age(row['date_of_birth'])
            print(f"Age: {age}")
            evaluate = ''
            if row['test_type'] == 'diabetes':
                if row['result'] < 100:
                    evaluate = 'Normal'
                elif 100 <= row['result'] <= 125:
                    evaluate = 'Pre-Diabetic'
                else:
                    evaluate = 'Diabetic'
            if row['test_type'] == 'uric_acid_urine':
                if row['result'] < 250:
                    evaluate = 'Low'
                elif 250 <= row['result'] <= 750:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'cholesterol':
                if row['result'] < 200:
                    evaluate = 'Desirable'
                elif 200 <= row['result'] <= 239:
                    evaluate = 'Borderline High'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'fasting_glucose':
                if row['result'] < 70:
                    evaluate = 'Low'
                elif 70 <= row['result'] <= 99:
                    evaluate = 'Normal'
                elif 100 <= row['result'] <= 125:
                    evaluate = 'Prediabetes'
                else:
                    evaluate = 'Diabetes'
            if row['test_type'] == 'hba1c':
                if row['result'] < 5.7:
                    evaluate = 'Normal'
                elif 5.7 <= row['result'] <= 6.4:
                    evaluate = 'Prediabetes'
                else:
                    evaluate = 'Diabetes'
            if row['test_type'] == 'serum_creatinine':
                if row['result'] < 0.7:
                    evaluate = 'Low'
                elif 0.7 <= row['result'] <= 1.3:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'total_bilirubin':
                if row['result'] < 0.1:
                    evaluate = 'Low'
                elif 0.1 <= row['result'] <= 1.2:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'ldl_cholesterol':
                if row['result'] < 100:
                    evaluate = 'Optimal'
                elif 100 <= row['result'] <= 129:
                    evaluate = 'Near Optimal'
                elif 130 <= row['result'] <= 159:
                    evaluate = 'Borderline High'
                elif 160 <= row['result'] <= 189:
                    evaluate = 'High'
                else:
                    evaluate = 'Very High'
            if row['test_type'] == 'hdl_cholesterol':
                if row['result'] < 40:
                    evaluate = 'Low'
                elif 40 <= row['result'] <= 59:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'triglycerides':
                if row['result'] < 150:
                    evaluate = 'Normal'
                elif 150 <= row['result'] <= 199:
                    evaluate = 'Borderline High'
                elif 200 <= row['result'] <= 499:
                    evaluate = 'High'
                else:
                    evaluate = 'Very High'
            if row['test_type'] == 'bun':
                if row['result'] < 7:
                    evaluate = 'Low'
                elif 7 <= row['result'] <= 20:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'alp':
                if row['result'] < 44:
                    evaluate = 'Low'
                elif 44 <= row['result'] <= 147:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'calcium':
                if row['result'] < 8.5:
                    evaluate = 'Low'
                elif 8.5 <= row['result'] <= 10.2:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            if row['test_type'] == 'wbc':
                if row['result'] < 4.0:
                    evaluate = 'Low'
                elif 4.0 <= row['result'] <= 11.0:
                    evaluate = 'Normal'
                else:
                    evaluate = 'High'
            report_name = str(uuid.uuid4())
            pdf_dir = os.path.join(settings.MEDIA_ROOT, 'reports', 'clients')
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports/clients', f'{report_name}.pdf')
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica", 18)
            x_start, y_start, y_offset = 50, 750, 55
            x_center = letter[0] / 2
            company_name = f"Big Data Project - Medical Lab System, {row['test_type']} Report"
            c.drawCentredString(x_center, y_start, company_name)
            c.line(50, y_start - y_offset, 550, y_start - y_offset)
            c.drawString(x_start, y_start - 3*y_offset, f"Patient Name: {row['patient_name']}")
            c.drawString(x_start, y_start - 4*y_offset, f"Phone Number: {row['phone_number']}")
            c.drawString(x_start, y_start - 5*y_offset, f"Email: {row['email']}")
            c.drawString(x_start, y_start - 6*y_offset, f"Test Type: {row['test_type']}")
            c.drawString(x_start, y_start - 7*y_offset, f"Result: {row['result']}")
            c.drawString(x_start, y_start - 8*y_offset, f"Evaluation: {evaluate}")
            c.drawString(x_start, y_start - 9*y_offset, f"Date of Birth: {row['date_of_birth']}")
            c.drawString(x_start, y_start - 10*y_offset, f"Age: {age}")
            c.drawString(x_start, y_start - 11*y_offset, f"Report Name: {report_name}")
            c.drawString(x_start, y_start - 12*y_offset, f"Payment: {row['payment']} USD")
            c.line(x_start, y_start - 13*y_offset, 550, y_start - 13*y_offset)
            c.showPage()
            c.save()
            models.ReportFile.objects.create(
                file=f'reports/clients/{report_name}.pdf',
                owner_name=row['patient_name'],
                owner_email=row['email'],
                report_type=row['test_type'],
                added_by=user
            )
            models.PatientReport.objects.create(
                patient_name=row['patient_name'],
                phone_number=row['phone_number'],
                patient_email=row['email'],
                test_type=row['test_type'],
                result=row['result'],
                evaluation=evaluate,
                filename=f'{report_name}.pdf',
                added_by=user,
                date_of_birth=row['date_of_birth'],
                age=age,
                payment=row['payment'],
                payment_status=row['payment_status']
            )
        print('Files uploaded to media folder')
    except Exception as e:
        print(f"Error processing file: {e}")
        
@login_required(login_url='/auth/login')        
def file_analysis_test(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.warning(
            request,
            message=f'You donot have access to these pages!',
            extra_tags='danger'
        )
        return redirect('/auth/dashboard')
    if request.method == 'POST':
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.added_by = request.user
            form.instance.file_category = 'diabetes'
            instance = form.save()  
            filename = instance.upload_name.name 
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            try:
                test_evaluation(filename=file_path, user=request.user)
                messages.success(
                    request,
                    message=f'File submitted! Evaluations are also saved in the system',
                    extra_tags='success'
                )
            except Exception as e:
                messages.error(
                    request,
                    message=f'Error processing file!\n{e}',
                    extra_tags='danger'
                )
            return redirect('/lab/test-upload')
        else:
            messages.warning(
                request,
                message=f'Your form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return redirect('/lab/test-upload')
    else:
        form = forms.FileUploadForm()
    return render(
        request,
        'LabApp/test-upload.html',
        {
            'form': form,
            'test_upload': True
        }
    )

@login_required(login_url='/auht/login')
def sample_generator(request):
    form = forms.SampleGenerationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.generated_by = request.user
            dataset_size = form.cleaned_data['dataset_size']
            filename = dataset_generator_driver_code(dataset_size)
            form.instance.filename = filename
            form.instance.record_size = dataset_size
            form.save()
            return redirect(filename)
        else:
            messages.warning(
                request,
                message=f'Your Form has errors!\n{form.errors}',
                extra_tags='danger'
            )
            return render(
                request,
                'LabApp/sample-dataset-generator.html',
                {
                    'form': form
                }
            )
    return render(
        request,
        'LabApp/sample-dataset-generator.html',
        {
            'form': form,
            'dataset_generator': True
        }
    )

    