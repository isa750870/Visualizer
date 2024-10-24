import unittest
from Vizualizator import generate_mermaid_graph, get_dependencies
class TestDependencyVisualizer(unittest.TestCase):

    def test_get_dependencies(self):
        dependencies = get_dependencies('curl')
        self.assertIn('libcurl4t64', dependencies)
        self.assertIn('zlib1g', dependencies)
        self.assertIn('libc6', dependencies)

    def test_generate_mermaid_graph(self):
        graph = generate_mermaid_graph({'libcurl4', 'libssl1.1'})
        expected = "graph TD\n    libcurl4\n    libssl1.1"
        self.assertEqual(graph, expected)

if __name__ == '__main__':
    unittest.main()