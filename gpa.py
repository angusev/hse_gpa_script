from bs4 import BeautifulSoup
import argparse


WORD2MARK = {'отлично': 5,
    'хорошо': 4,
    'зачёт': 3
}


def get_gpas(soup):
    table = soup.find('tbody')

    table_elems = list(table.children)

    gpa5 = 0.
    gpa10 = 0.
    total_credits = 0

    print('SUBJECT'.ljust(70), '', '', 'CREDITS', sep='\t')
    for i in range(len(table_elems)):
        if table_elems[i].name == 'tr':
            subject_tags = list(table_elems[i].children)
            for j in range(2, len(subject_tags)):
                str_mark5 = subject_tags[j].string
                str_mark10 = subject_tags[j-2].string

                if str_mark5 in WORD2MARK.keys() and str_mark10:
                    mark10 = int(str_mark10)
                    mark5 = WORD2MARK[str_mark5]

                    credits = int(subject_tags[j-3].string)
                    gpa5 += mark5 * credits
                    gpa10 += mark10 * credits
                    total_credits += credits

                    print(subject_tags[j-11].string.ljust(70, '_'), str_mark5, str_mark10, credits, sep='\t')

    print('TOTAL CREDITS:'.ljust(70), '', '', total_credits, sep='\t')
    print()
    gpa5 /= total_credits
    gpa10 /= total_credits
    return gpa5, gpa10


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', type=str, default='LMS HSE.html')
    args = parser.parse_args()

    with open(args.filename, 'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    gpas = get_gpas(soup)

    print(f'GPA: {round(gpas[0], 2)}/5.0, {round(gpas[1], 2)}/10.0')
