import subprocess
import xml.etree.ElementTree as ET
import sys
import os

def get_package_dependencies(package_name):
    #Получаем зависимости с помощью apt-depends и рекурсии
    try:
        result = subprocess.run(
            ['apt-cache', 'depends', package_name],
            capture_output=True, text=True, check=True
        )
        output = result.stdout
        dependencies = []
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("Depends:") or line.startswith("Recommends:"):
                dep = line.split()[1]
                dependencies.append(dep)
        return dependencies
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении зависимости для {package_name}: {e}")
        return []

def create_mermaid_graph(package_name, dependencies):
    #Создание кода графа в формате Mermaid
    graph_code = f"graph TD\n"
    for dep in dependencies:
        graph_code += f"    {package_name} --> {dep}\n"
    return graph_code

def generate_graphviz(package_name, dependencies):
    #Генерация кода графа для программы визуализатора Graphviz
    dot_output = f'digraph "{package_name}" {{\n'
    dot_output += f'    "{package_name}" [shape=box];\n'

    for dep in dependencies:
        dot_output += f'    "{package_name}" -> "{dep}" [shape=box];\n'

    dot_output += "}\n"
    return dot_output

def save_graph_to_png(dot_file, graphviz_path):
    #Генерация png файла с графом зависимостей
    try:
        subprocess.run(
            [graphviz_path, '-Tpng', dot_file, '-o output.png'],
            check=True
        )
        print(f"Граф успешно сохранен в output.png")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании изображения: {e}")

def main():
    if len(sys.argv) != 4:
        print("Использование: python program.py <graphviz_path> <package_name> <output_mmd_path>")
        sys.exit(1)

    graphviz_path = sys.argv[1]
    package_name = sys.argv[2]
    output_file = sys.argv[3]

    print(f"Путь к Graphviz: {graphviz_path}")
    print(f"Имя пакета: {package_name}")
    print(f"Имя файла вывода: {output_file}")
    print(f"Имя файла изображения: output.png")

    print("Получение зависимостей пакета...")
    dependencies = get_package_dependencies(package_name)
    print(f"Зависимости: {dependencies}")

    if dependencies:
        dot_graph = generate_graphviz(package_name, dependencies)
        dot_filename = f"{package_name}_dependencies.dot"

        with open(dot_filename, 'w') as f:
            f.write(dot_graph)
        graph_code = create_mermaid_graph(package_name, dependencies)
        print("Код вида Mermaid:")
        print(graph_code)

        with open(output_file, 'w') as f:
            f.write(graph_code)
        print("Создание PNG изображения...")
        save_graph_to_png(dot_filename, graphviz_path)

        os.remove(f"{package_name}_dependencies.dot")
    else:
        print(f"Не удалось получить зависимости для пакета {package_name}.")

if __name__ == "__main__":
    main()
