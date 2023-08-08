from setuptools import setup, find_packages

setup(
    name='TelegramContract2vCard',
    version='1.0.1',
    description='make telegram contacts.html or result.json to vCard automatically',
    author='jjh4450',
    author_email='jjh4450git@gmail.com',
    url='https://github.com/jjh4450/TelegramContract2vCard',
    install_requires=["beautifulsoup4"],
    packages=find_packages(exclude=[]),
    keywords=['telegram', 'contacts', 'vcf', 'vcard', 'html', 'json', 'parser'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)