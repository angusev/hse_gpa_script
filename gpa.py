from bs4 import BeautifulSoup
import argparse
from os import listdir
from os.path import isfile, join


WORD2MARK = {'отлично': 5,
    'хорошо': 4,
    'удовлетворительно': 3
}


def get_gpas(soup, newdesign):
    tables = soup.find_all('tbody')

    gpa5 = 0.
    gpa10 = 0.
    total_credits = 0
    print('SUBJECT'.ljust(70), '', '', 'CREDITS', sep='\t')

    if newdesign:
        SUB_DIF = 0
        CRED_DIF = 3
        MAR10_DIF = 1
    else:
        SUB_DIF = 11
        CRED_DIF = 3
        MAR10_DIF = 2

    for table in tables:
        table_elems = list(table.children)

        for i in range(len(table_elems)):
            table_elem = table_elems[i]
            if table_elem.name == 'tr':
                subject_tags = list(table_elem.children)

                for j in range(2, len(subject_tags)):
                    str_mark5 = subject_tags[j].string
                    str_mark10 = subject_tags[j - MAR10_DIF].string

                    if str_mark5 in WORD2MARK.keys() and str_mark10:
                        mark10 = int(str_mark10)
                        mark5 = WORD2MARK[str_mark5]

                        credits = int(subject_tags[j - CRED_DIF].string)
                        gpa5 += mark5 * credits
                        gpa10 += mark10 * credits
                        total_credits += credits

                        sub_name = subject_tags[j - SUB_DIF].string
                        if newdesign:
                            sub_name = subject_tags[0].get_text()
                        print(sub_name.ljust(70, '_'), 
                            str_mark5[:3], str_mark10, credits, sep='\t')

    print('TOTAL CREDITS:'.ljust(70), '', '', total_credits, sep='\t')
    print()
    gpa5 /= total_credits
    gpa10 /= total_credits
    return gpa5, gpa10, total_credits


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', type=str, default='LMS HSE.html')
    parser.add_argument('--folder', type=str, default='./lms_new/')
    parser.add_argument('--newdesign', action='store_true', default=False)
    args = parser.parse_args()

    if args.newdesign:
        files = [f for f in listdir(args.folder) if isfile(join(args.folder, f))]
        gpa5 = 0.
        gpa10 = 0.
        total_credits = 0

        for file in files:
            with open(args.folder + file, 'r') as f:
                html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')

            results = get_gpas(soup, args.newdesign)
            gpa5 += results[0] * results[2]
            gpa10 += results[1] * results[2]
            total_credits += results[2]

        gpa5 /= total_credits
        gpa10 /= total_credits
        print(f'GPA: {round(gpa5, 2)}/5.0, {round(gpa10, 2)}/10.0')

    else:
        with open(args.filename, 'r') as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')

        gpas = get_gpas(soup, args.newdesign)

        print(f'GPA: {round(gpas[0], 2)}/5.0, {round(gpas[1], 2)}/10.0')
