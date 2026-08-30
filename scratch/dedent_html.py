import os
import re
import textwrap

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find st.markdown(f'''...''' or st.markdown('''...'''
    # We use a non-greedy match for the string content
    pattern = re.compile(r'(st\.markdown\(\s*[f]?[\"\'\']{3})(.*?)([\"\'\']{3}\s*,?\s*unsafe_allow_html=True\s*\))', re.DOTALL)
    
    def replacer(match):
        prefix = match.group(1)
        body = match.group(2)
        suffix = match.group(3)
        # only dedent if there's an HTML tag
        if '<div' in body or '<span' in body or '<p' in body or '<h' in body or '<table' in body:
            lines = body.split('\n')
            if len(lines) > 1 and lines[0].strip() == '':
                rest = '\n'.join(lines[1:])
                dedented = '\n' + textwrap.dedent(rest)
            else:
                dedented = textwrap.dedent(body)
            return prefix + dedented + suffix
        return match.group(0)

    new_content = pattern.sub(replacer, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed {filepath}')

for root, dirs, files in os.walk('d:/SEMESTER 5/PROJEK/geo_smart_streamlit/views'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))
