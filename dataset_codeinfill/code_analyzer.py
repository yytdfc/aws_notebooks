from tree_sitter import Language, Parser

def get_language(language_name):
    """Get the tree-sitter Language object for the specified language."""
    if language_name == 'python':
        import tree_sitter_python as tspython
        return Language(tspython.language())
    elif language_name == 'java':
        import tree_sitter_java as tsjava
        return Language(tsjava.language())
    elif language_name == 'javascript':
        import tree_sitter_javascript as tsjavascript
        return Language(tsjavascript.language())
    elif language_name == 'cpp':
        import tree_sitter_cpp as tscpp
        return Language(tscpp.language())
    else:
        raise ValueError(f"Unsupported language: {language_name}")

def create_parser(language_name):
    """Create a parser for the specified language."""
    parser = Parser(get_language(language_name))
    return parser


def analyze_code(code_snippet, language='python'):
    """
    Analyze code using tree-sitter parser.
    Returns the original code as a list of tokens.
    """
    language = language.lower()
    language_map = {
        'python': 'python',
        'py': 'python',
        'java': 'java',
        'javascript': 'javascript',
        'js': 'javascript',
        'c': 'cpp',
        'c++': 'cpp',
        'cpp': 'cpp'
    }
    
    if language not in language_map:
        raise ValueError(f"Unsupported language: {language}")
    
    parser = create_parser(language_map[language])
    tree = parser.parse(bytes(code_snippet, "utf8"))
    
    # Get all nodes in order of appearance
    nodes = []
    cursor = tree.walk()
    reached_end = False

    while not reached_end:
        nodes.append(cursor.node)
        
        if cursor.goto_first_child():
            continue
            
        if cursor.goto_next_sibling():
            continue
            
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_end = True
            elif cursor.goto_next_sibling():
                retracing = False
    
    # Filter for leaf nodes only and sort by start byte
    leaf_nodes = [node for node in nodes if len(node.children) == 0]
    leaf_nodes.sort(key=lambda x: x.start_byte)
    
    # Extract text from leaf nodes
    tokens = []
    last_end = 0
    
    for node in leaf_nodes:
        # Add any whitespace between nodes
        if node.start_byte > last_end:
            tokens.append(code_snippet[last_end:node.start_byte])
        tokens.append(code_snippet[node.start_byte:node.end_byte])
        last_end = node.end_byte
    
    # Add any remaining whitespace at the end
    if last_end < len(code_snippet):
        tokens.append(code_snippet[last_end:])
    
    return tokens

# Example usage
if __name__ == "__main__":
    python_code = """
def hello(name):
    print(f"Hello, {name}!")

hello("World")
"""
    
    java_code = """
public class HelloWorld {
    @Override
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""

    javascript_code = """
function greet(name) {
    console.log(`Hello, ${name}!`);
}

greet("World");
"""

    cpp_code = """
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""

    print("Python code analysis:")
    result = analyze_code(python_code, 'python')
    print("".join(result))
    
    print("\nJava code analysis:")
    result = analyze_code(java_code, 'java')
    print("".join(result))

    print("\nJavaScript code analysis:")
    result = analyze_code(javascript_code, 'javascript')
    print("".join(result))

    print("\nC++ code analysis:")
    result = analyze_code(cpp_code, 'cpp')
    print("".join(result))

