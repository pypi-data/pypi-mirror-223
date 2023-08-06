from setuptools import setup, find_packages

setup(
    name="async-message-server",
    version="0.0.1",
    description="study gb async-message-server",
    packages=find_packages(),
    author="Mytsykov Sergey",
    author_email="smytsykov@gmail.com",
    url="https://github.com/LuckyBustard/async_chat_gb",
    install_requires=['PyQt6', 'sqlalchemy'],
)
