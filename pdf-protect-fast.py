from PyPDF2 import PdfFileWriter, PdfFileReader

import os
import PyPDF2
##from tqdm import tqdm
import concurrent.futures
from random import randint
import time

def display_instructions():
    print('Instructions:\n  1. Put all the pdfs you want to encrypt into a folder\n  2. Put this .py script into that same folder\n')

    pdflist = [f for f in os.listdir('./') if f.endswith('.pdf')]

    print(f"Found {len(pdflist)} pdf files in the current folder {os.path.abspath('./')}\n")

    return pdflist

def exit_msg(protected_dir, password):
    print(f'Your pdfs are protected with password {password} and are in the \'{protected_dir}\' folder')
    input('Press Enter/Return to exit.')

def create_password(length=8):
    pword = input('What password do you want to use? (Press Enter/Return without a password for a randomly generated one): ').strip()

    total_alphas = list('ABCDEVWXYZ0123456789')
    pw_len = length
    pword = pword if len(pword)>0 else ''.join([total_alphas[randint(0,len(total_alphas)-1)] for i in range(pw_len)])

    pf = open(f'./Password is {pword}.txt','w')
    pf.write(f'Password is {pword}')
    pf.close()
    return pword

def add_encryption(input_pdf, output_pdf, password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf, strict=False)

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    pdf_writer.encrypt(user_pwd=password, owner_pwd=None, 
                       use_128bit=True)

    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)

    return output_pdf

if __name__ == '__main__':
    pdflist = display_instructions()
    if not pdflist:
        print('no pdfs to encrypt.')
        input('Press Enter/Return to exit.')
    else:
        newfoldername = os.path.join('.', 'protected')
        if not os.path.exists(newfoldername):
            os.mkdir(newfoldername)
        password = create_password()

##        for i in range(len(pdflist)):
##            fname = pdflist[i]
##            add_encryption(
##                os.path.join('.', fname),
##                os.path.join(newfoldername, fname),
##                password
##            )
##        exit_msg(newfoldername, password)
        t1 = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for pdf in pdflist:
                futures.append(
                    executor.submit(
                        add_encryption,
                        input_pdf=os.path.join('.', pdf),
                        output_pdf=os.path.join(newfoldername, pdf),
                        password=password
                    )
                )
            for future in concurrent.futures.as_completed(futures):
                print('encrypted', future.result())
        t2 = time.time()
        print('Time taken:', t2 - t1)
        exit_msg(newfoldername, password)
