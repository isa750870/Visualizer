import subprocess
import sys
import argparse

def get_dependencies(package):
    """Получает зависимости пакета и его транзитивные зависимости."""
    command = f"apt-cache depends {package}"
    output = subprocess.check_output(command, shell=True, text=True)
    
    dependencies = set()
    
    for line in output.splitlines():
        if 'Depends:' in line:
            dep = line.split('Depends:')[1].strip()
            dependencies.add(dep.split()[0])  # Берем только имя пакета
            
    return dependencies

def generate_mermaid_graph(dependencies):
    """Генерирует код графа в формате Mermaid."""
    graph = ["graph TD"]
    for dep in dependencies:
        graph.append(f"    {dep}")
    
    return '\n'.join(graph)

def main():
    parser = argparse.ArgumentParser(description="Visualization of package dependencies in Ubuntu.")
    parser.add_argument('--path', required=True, help='Path to the visualizer program.')
    parser.add_argument('--package', required=True, help='Name of the package to analyze.')
    parser.add_argument('--output', required=True, help='Path to the output file for the Mermaid code.')
    
    args = parser.parse_args()
    
    # Получаем зависимости
    dependencies = get_dependencies(args.package)
    
    # Генерируем граф в формате Mermaid
    mermaid_code = generate_mermaid_graph(dependencies)
    
    # Выводим на экран
    print(mermaid_code)
    
    # Записываем в файл
    with open(args.output, 'w') as f:
        f.write(mermaid_code)

if __name__ == "__main__":
    main()