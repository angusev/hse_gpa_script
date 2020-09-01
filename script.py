from bs4 import BeautifulSoup
import argparse


WORD2MARK = {'отлично': 5,
    'хорошо': 4,
    'зачёт': 3
}


def get_gpa(soup, scale=10):
    table = soup.find('tbody')

    table_elems = list(table.children)

    gpa = 0.
    total_credits = 0

    for i in range(len(table_elems)):
        if table_elems[i].name == 'tr':
            subject_tags = list(table_elems[i].children)
            for j in range(len(subject_tags)):

                if subject_tags[j].string in WORD2MARK.keys() and subject_tags[j-2].string:
                    if scale == 10:
                        mark = int(subject_tags[j-2].string)
                    elif scale == 5:
                        mark = WORD2MARK[subject_tags[j].string]
                    else:
                        raise ValueError('Unknown scale')

                    credits = int(subject_tags[j-3].string)
                    gpa += mark * credits
                    total_credits += credits

    gpa /= total_credits
    return gpa


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', type=str, default='LMS HSE.html')
    parser.add_argument('--scale', type=float, default=10.)
    args = parser.parse_args()

    with open(args.filename, 'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    gpa = get_gpa(soup, args.scale)

    print(f'GPA: {round(gpa, 2)}/{args.scale}')