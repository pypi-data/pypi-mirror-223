from setuptools import setup, find_packages

setup(
    name='Linguify',
    version='2.5.0',
    packages=find_packages(),
    package_data={'linguify': ['credentials.json']},
    install_requires=[
    "openai",
    "python-docx",
    "google-api-python-client",
    "google-auth-httplib2",
    "google-auth-oauthlib",
    "click"
    ],
    entry_points={"console_scripts": ["linguify=linguify:start"]},

    author='Abdulrahman Khafagy',
    author_email='abdul_khafagy2004@hotmail.com',
    description='Linguify is designed to automate voicemail transcription via email parsing.',
)


