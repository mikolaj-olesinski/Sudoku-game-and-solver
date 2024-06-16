from setuptools import setup, find_packages

setup(
    name='SudokuGameAndSolver', 
    version='0.1', 
    packages=find_packages(),  
    install_requires=[
        'numpy==1.23.5',
        'opencv-python==4.7.0.72',
        'PySide6==6.5.0',
        'protobuf==3.20.3',
        'tensorflow==2.12.0',
        'sqlalchemy==2.0.0',
    ],
    entry_points={
        'console_scripts': [
            # 'nazwa_komendy=modul:funkcja',  # Przykład dodania skryptu konsolowego
        ],
    },
    python_requires='>=3.6',
)
