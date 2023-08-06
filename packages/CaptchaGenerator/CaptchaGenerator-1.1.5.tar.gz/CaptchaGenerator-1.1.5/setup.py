from setuptools import setup

setup(
    long_description = """
    # <a href="https://github.com/Sepehr0Day/CaptchaGenerator/">You can see library info in my github</a>'
    """,
    long_description_content_type = "text/markdown",
    name='CaptchaGenerator',
    version='1.1.5',
    license='MIT',
    description='A library for captcha generator for Telegram bots',
    author='Sepehr0Day',
    author_email='sphrz2324@gmail.com',
    packages=['CaptchaGenerator'],
    install_requires=[
        'Pillow',
        'colorama',
    ],
)