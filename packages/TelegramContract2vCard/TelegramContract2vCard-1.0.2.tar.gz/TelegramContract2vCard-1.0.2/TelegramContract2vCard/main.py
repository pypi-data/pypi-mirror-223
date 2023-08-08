from bs4 import BeautifulSoup
from itertools import zip_longest
import json


def html2dict(html_dir: str) -> dict:
    """
        Change telegram contacts.html(default name) to python dict

        Args:
            html_dir (str): path to contacts.html

        Returns:
            contacts (dict): dict of dict
            dict = {
                'name':{
                    'phone': str,
                    'date': str
                }
            }
            
    """
    contacts = {}
    with open(html_dir, 'r', encoding='UTF8') as f:
        data = f.read()
        soup = BeautifulSoup(data, 'html.parser')
        names = map(lambda s: s.text.strip(), soup.find_all('div', class_='name bold'))
        phones = map(lambda s: s.text.strip(), soup.find_all('div', class_='details_entry details'))
        date_ = map(lambda s: s.text.strip(), soup.find_all('div', class_='pull_right info details'))
        for name, phone, date in zip_longest(names, phones, date_):
            contacts[name] = {
                'phone': phone,
                'date': date,
            }

    return contacts


def json2dict(json_dir: str, fill_mid_of_name='') -> dict:
    """
        Change telegram result.json(default name) to python dict

        Args:
            json_dir (str): path to contacts.json
            fill_mid_of_name (str): fill mid of name    ex) ' '

        Returns:
            contacts (dict): dict of dict
            dict = {
                'name':{
                    'phone': str,
                    'date': str
                }
            }

    """
    contacts = {}
    with open(json_dir, 'r', encoding='UTF8') as f:
        data = json.load(f)
        for i in data['contacts']['list']:
            name = i['first_name'] + fill_mid_of_name + i['last_name']
            phone = i['phone_number']
            date = i['date']
            contacts[name] = {
                'phone': phone,
                'date': date,
            }
    return contacts


def html2vcf(html_dir: str, filename: str = "my_contacts", vcf_dir: str = '.') -> None:
    """
        Change telegram contacts.html(default name) to vcf file

        Args:
            html_dir (str): path to contacts.html
            filename (str): name of vcf file
            vcf_dir (str): directory to save vcf file

        Returns:
            None
    """
    contacts = html2dict(html_dir)
    dict2vcf(contacts, filename, vcf_dir)


def json2vcf(json_dir: str, filename: str = "my_contacts", vcf_dir: str = '.', fill_mid_of_name='') -> None:
    """
        Change telegram result.json(default name) to vcf file

        Args:
            json_dir (str): path to contacts.json
            filename (str): name of vcf file
            vcf_dir (str): directory to save vcf file
            fill_mid_of_name (str): fill mid of name    ex) ' '

        Returns:
            None
    """
    contacts = json2dict(json_dir, fill_mid_of_name)
    dict2vcf(contacts, filename, vcf_dir)


def dict2vcf(data: dict, filename: str = "my_contacts", vcf_dir: str = '.') -> None:
    """
        Change contacts dict to vcf file

        Args:
            data: contacts dict that made by html2dict or json2dict
            filename: name of vcf file
            vcf_dir (str): directory to save vcf file

        Returns: vcf file in current directory

    """
    vcard_template = "BEGIN:VCARD\nVERSION:3.0\nN:{}\nTEL:{}\nEND:VCARD\n"

    vcard_list = []
    for name, value in data.items():
        phone = value['phone']
        vcard_list.append(vcard_template.format(name, phone))

    vcard_string = "\n".join(vcard_list)

    with open(f"{vcf_dir}/{filename}.vcf", 'w', encoding='utf-8') as vcf_file:
        vcf_file.write(vcard_string)


if __name__ == "__main__":
    pass
    # print(json2dict('result.json'))
    # print(html2dict('contacts.html'))
    # json2vcf('result.json')
