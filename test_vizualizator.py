import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import os
from Vizualizator import get_package_dependencies, create_mermaid_graph, generate_graphviz, save_graph_to_png, main

class TestVisualizer(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_package_dependencies_success(self, mock_run):
        # Настройка имитации для успешного вызова subprocess
        mock_run.return_value = MagicMock(stdout='Depends: libA\nDepends: libB\nRecommends: libC\n', returncode=0)
        
        result = get_package_dependencies('some-package')
        
        self.assertEqual(result, ['libA', 'libB', 'libC'])

    @patch('subprocess.run')
    def test_get_package_dependencies_failure(self, mock_run):
        # Настройка имитации для вызова subprocess с ошибкой
        mock_run.side_effect = subprocess.CalledProcessError(1, 'apt-cache depends')
        
        result = get_package_dependencies('nonexistent-package')
        
        self.assertEqual(result, [])
        
    def test_create_mermaid_graph(self):
        package_name = 'some-package'
        dependencies = ['libA', 'libB', 'libC']
        
        expected_graph = (
            "graph TD\n"
            "    some-package --> libA\n"
            "    some-package --> libB\n"
            "    some-package --> libC\n"
        )
        
        result = create_mermaid_graph(package_name, dependencies)
        self.assertEqual(result, expected_graph)

    def test_generate_graphviz(self):
        package_name = 'some-package'
        dependencies = ['libA', 'libB']
        
        expected_dot = (
            'digraph "some-package" {\n'
            '    "some-package" [shape=box];\n'
            '    "some-package" -> "libA" [shape=box];\n'
            '    "some-package" -> "libB" [shape=box];\n'
            '}\n'
        )
        
        result = generate_graphviz(package_name, dependencies)
        self.assertEqual(result, expected_dot)

    @patch('subprocess.run')
    def test_save_graph_to_png_success(self, mock_run):
        # Настройка имитации для успешного вызова subprocess
        mock_run.return_value = MagicMock(returncode=0)
        
        result = save_graph_to_png('dummy.dot', 'dummy_path')
        
        # Проверяем, что subprocess.run был вызван с ожидаемыми аргументами
        mock_run.assert_called_once_with(['dummy_path', '-Tpng', 'dummy.dot', '-o output.png'], check=True)

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
