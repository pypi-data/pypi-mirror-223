from setuptools import setup, find_packages

with open('ashcrypt/README.md', 'r') as f:
    readme = f.read()

setup(
    name='ashcrypt',
    version='3.2.1',
    author='Ashref Gwader',
    author_email='AshrefGw@proton.me',
    python_requires='>=3.7',
    description="Comprehensive AES-256 Cryptography App & library equipped with files & text handling modules along"
                " with a database module to store encrypted content.",
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://github.com/AshGw/AES-256.git',
    packages=find_packages(exclude=['important', 'Docker-build', '.github']),
    package_data={
        'ashcrypt': ['**'],
    },
    exclude_package_data={
        '': ['.gitignore', 'LICENSE', 'README.md'],
    },
    install_requires=[
        'bcrypt==4.0.1',
        'cryptography==40.0.2',
        'qrcode==7.4.2',
        'ttkbootstrap==1.10.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords=[
        'Cryptography application',
        'cryptography library'
        'AES-256',
    ],
)
